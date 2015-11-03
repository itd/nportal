import logging
from sqlalchemy.exc import OperationalError
import pyramid.config as pcon

from pyramid.security import (
    Allow,
    Deny,
    Authenticated,
    Everyone,
    remember,
    forget,
    DENY_ALL
    )

from sqlalchemy.orm import (scoped_session, sessionmaker)
from zope.sqlalchemy import ZopeTransactionExtension
from time import time

from pyramid.exceptions import ConfigurationError
from pyramid.security import Allow, Authenticated

import ldap3
from ldap3 import (Server, Connection, AUTH_SIMPLE,
                   STRATEGY_SYNC, STRATEGY_ASYNC_THREADED, Tls,
                   SEARCH_SCOPE_WHOLE_SUBTREE, SEARCH_SCOPE_SINGLE_LEVEL,
                   ALL_ATTRIBUTES, GET_ALL_INFO)

logger = logging.getLogger(__name__)


_ord = ord if str is bytes else int
# settings = request.registry.settings


LDAP_SERVER = Server('ds1.nrel.gov', port=389, use_ssl=False)
#LDAP_SERVER = Server('ds.nrel.gov', port=683, use_ssl=True)
#LDAP_PORT = '389'
LDAP_USER = 'adread@nrel.gov'
LDAP_PASS = '4wardPa55'
BASEDN = 'OU=Scientific Computing,DC=nrel,DC=gov'


class RootFactory(object):
    __acl__ = [
        (Allow, Authenticated, 'view'),
        (Allow, 'group:editors', 'edit'),
        (Allow, 'group:admin', 'add'),
        (Allow, 'group:admin', 'edit'),
        (Allow, 'group:admin', 'delete'),
        ]

    def __init__(self, request):
        pass


def groupfinder(userdn, request):
    """Groupfinder function for Pyramid.

    A groupfinder implementation useful in conjunction with out-of-the-box
    Pyramid authentication policies.  It returns the DN of each group
    belonging to the user specified by ``userdn`` to as a principal
    in the list of results; if the user does not exist, it returns None.
    """
    groups = get_groups(userdn, request)
    if groups:
        groups = [r[0] for r in groups]
    return groups


def get_groups(userdn, request):
    """Raw groupfinder function returning the complete group query result."""
    connector = get_ldap_connector(request)
    return connector.user_groups(userdn)


def get_ldap_connector(request):
    """Return the LDAP connector attached to the request.

    If :meth:`pyramid.config.Configurator.ldap_setup` was not called, using
    this function will raise an :exc:`pyramid.exceptions.ConfigurationError`.
    """
    connector = getattr(request, 'ldap_connector', None)
    if connector is None:
        if ldap3.LDAPException is Exception:  # pragma: no cover
            raise ImportError(
                'You must install ldap3 to use an LDAP connector.')
        raise ConfigurationError(
            'You must call Configurator.ldap_setup during setup '
            'to use an LDAP connector.')
    return connector


# def groupfinder(userid, request):
#     sess = DBSession()
#     user = sess.query(Users).filter_by(userid=userid).one()
#     roleid = user.role
#     role = sess.query(RoleModel).filter_by(roleid=roleid).one()
#
#     return ['group:' + role.rolename]

#
# def user_list():
#     sess = DBSession()
#     users = sess.query(Users).order_by(Users.userid).all()
#     users = {i.userid: i.role for i in users}
#     rdata = sess.query(RoleModel).all()
#     roles = {i.roleid: i.rolename for i in rdata}
#     for user in users:
#         users[user] = roles[users[user]]
#     return users


def check_user_login(login, password):
    userdata = getuserdata(login)

    if not userdata:
        return False

    dn = userdata['distinguishedName'][0]
    auth_check = user_auth_check(dn, login, password)
    return dict(auth=auth_check, dn=dn, uid=login)


def user_auth_check(dn, login, password):
    server = LDAP_SERVER  # getInfo=GET_ALL_INFO
    # Hack. If it binds, the userid/password combo is good.
    conn = Connection(server, auto_bind=False,
                      client_strategy=STRATEGY_SYNC,
                      #client_strategy=STRATEGY_ASYNC_THREADED,
                      user=dn,
                      password=password,
                      authentication=AUTH_SIMPLE
                      )
    conn.open()
    res = conn.bind()

    if res:
        return True
    return False


def getuserdata(login):
    server = LDAP_SERVER  # getInfo=GET_ALL_INFO
    attributes = ['uid', 'distinguishedName', 'cn',
                  'mail', 'telephoneNumber',
                  'department', 'gidNumber', 'uidNumber']
    # basedn = 'OU=Accounts,DC=nrel,DC=gov'
    basedn = 'DC=nrel,DC=gov'
    search_filter = '(uid=%s)' % login
    # define a synchronous connection with basic authentication

    conn = Connection(server, auto_bind=True,
                      client_strategy=STRATEGY_ASYNC_THREADED,
                      user=LDAP_USER, password=LDAP_PASS,
                      authentication=AUTH_SIMPLE)
    ##client_strategy=STRATEGY_SYNC

    #conn.tls = tls()
    #conn.start_tls()

    result = conn.search(basedn, search_filter=search_filter,
                         search_scope=SEARCH_SCOPE_WHOLE_SUBTREE,
                         attributes=attributes )
    conn.get_response(result, timeout=10)
    data = conn.response

    # Check if a dict was returned,
    # meaning loginID is in LDAP and password works.
    if not data:
        return False

    # User has passed LDAP auth...
    # Finally, return the user's attribs.
    dn = data[0]['attributes']
    return dn

