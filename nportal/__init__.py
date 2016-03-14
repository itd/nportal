import os
import ldap3

from pyramid.config import Configurator
from pyramid.renderers import JSONP

from sqlalchemy import engine_from_config
from pyramid.session import SignedCookieSessionFactory

from .models import (
    DBSession,
    Base,
    )

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated
from security import groupfinder


def expandvars_dict(settings):
    """Expands all environment variables in a settings dictionary."""
    return dict((key, os.path.expandvars(value)) for
                key, value in settings.iteritems())


class RootFactory(object):
    __acl__ = [(Allow, Authenticated, 'view')]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    # get setting info from OS
    settings = expandvars_dict(settings)

    # Testing only. Change this out when in production
    req_session_factory = SignedCookieSessionFactory('somerandomstringforreq')

    # CAPTCHA TESTING: Change these out when in production:
    config = Configurator(settings=settings,
                          session_factory=req_session_factory)

    config.include('pyramid_chameleon')
    # config.include('pyramid_ldap3')
    # config.include('.security')
    # config.set_authentication_policy(
    #     AuthTktAuthenticationPolicy('CHANGE_THIS_seekr1t',
    #                                 callback=groupfinder))
    # config.set_authorization_policy(ACLAuthorizationPolicy())

    LDAP_READ = settings['ldap_read']
    LDAP_PASS = settings['ldap_pass']

    # config.ldap_setup(
    #     'ldap://ds1.hpc.nrel.gov',
    #     bind=settings['ldap_read'],
    #     passwd=settings['ldap_pass']
    # )
    #
    # config.ldap_set_login_query(
    #     base_dn='cn=users,cn=accounts,dc=hpctest,dc=nrel,dc=gov',
    #     filter_tmpl='(uid=%(login)s)',
    #     scope=ldap3.SEARCH_SCOPE_SINGLE_LEVEL
    # )
    #
    # config.ldap_set_groups_query(
    #     base_dn='dc=hpctest, dc=nrel, dc=gov',
    #     filter_tmpl='(&(objectCategory=group)(member=%(userdn)s))',
    #     scope=ldap3.SEARCH_SCOPE_WHOLE_SUBTREE,
    #     cache_period=600)

    config.add_route('nportal.login', '/login')
    config.add_route('nportal.logout', '/logout')

    config.add_renderer('jsonp', JSONP(param_name='callback'))
    config.add_renderer(name='csv',
                        factory='nportal.views.CSVRenderer')

    # views
    config.add_static_view('static', 'static', cache_max_age=1)
    config.add_static_view('deform', 'deform:static')
    #config.add_static_view('static', 'static', cache_max_age=1)
    #  3600

    config.add_route('home', '/')
    config.add_route('changepass', '/changepass')
    config.add_route('request_account', '/request_account')
    config.add_route('request_received_view', '/request_received/{unid}')

    config.add_route('admin_home', '/radmin')
    config.add_route('admin_request_edit', '/radmin/request_edit')
    config.add_route('req_list', '/radmin/requests')
    config.add_route('req_edit', '/radmin/request/{unid}')

    config.scan()
    return config.make_wsgi_app()
