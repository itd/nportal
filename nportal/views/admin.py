import os
from datetime import datetime
import string
from hashids import Hashids
import requests
import transaction
import ldap3

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import (scoped_session, sessionmaker)
from nportal.security import get_ldap_connector
# from pyramid_ldap3 import get_ldap_connector

from pyramid.response import Response

from pyramid.view import forbidden_view_config
from pyramid.security import remember, forget

from pyramid.decorator import reify
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPMovedPermanently,
    HTTPNotFound,
    )

from pyramid.session import SignedCookieSessionFactory

from pyramid.config import (Configurator, settings)

from pyramid.view import view_config
from pyramid.renderers import get_renderer, render, render_to_response
# from sqlalchemy.exc import DBAPIError
# import deform
from deform import (ZPTRendererFactory,
                    Form,
                    widget,
                    ValidationFailure)
    # decorator, default_renderer, field, form,
import colander
from pkg_resources import resource_filename

from nportal.models import (
    DBSession,
    Request,
    CountryCodes,
    # Citizenship
    )

from schemas import AddAccountSchema
from validators import uid_validator
from .lists import (us_states,
                    country_codes,
                    title_prefixes,
                    has_account,
                    )

# sqlalchemy setup
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),
                                        expire_on_commit=False))
# sess = DBSession()

# view flash session info
req_session_factory = SignedCookieSessionFactory('itsaseekreet')
config = Configurator()
config.set_session_factory(req_session_factory)

# deform retail form additions
resource_registry = widget.ResourceRegistry()
deform_templates = resource_filename('deform', 'templates')
tpath = os.getcwd()
search_path = (tpath + '/nportal/templates', deform_templates)
drenderer = ZPTRendererFactory(search_path)
# Form.set_zpt_renderer(search_path)
# import htmllaundry
# from htmllaundry import sanitize


def site_layout():
    renderer = get_renderer("../templates/_layout_admin.pt")
    layout = renderer.implementation().macros['layout']
    return layout


def add_base_template(event):
    base = get_renderer('templates/_layout.pt').implementation()
    event.update({'base': base})


class AdminViews(object):
    """
    """
    def __init__(self, request):
        self.request = request
        # renderer = get_renderer("../templates/_layout.pt")
        # self.layout = renderer.implementation().macros['layout']
        self.layout = site_layout()
        self.title = "Request Admin Views"

    @reify
    def account_req_form(self):
        schema = AddAccountSchema().bind(
            country_codes_data=country_codes,
            us_states_data=us_states
        )
        return Form(schema, buttons=('submit',))

    @reify
    def reqts(self):
        return self.account_req_form.get_widget_resources()

    @view_config(route_name='admin_home',
                 renderer='../templates/admin_home.pt',
                 permission='view')
    def admin_home(self):
        """
        The URL is /radmin
        """
        title = "Admin Home"
        return dict(page_title=self.title, title=title)

    @view_config(route_name='nportal.logout',
                 renderer='../templates/logout.pt')
    def logout(self):
        headers = forget(self.request)
        return Response('Logged out', headers=headers)

    @view_config(route_name='nportal.login',
                 renderer='../templates/login.pt')
    @forbidden_view_config(renderer='../templates/login.pt')
    def login(self):
        request = self.request
        referrer = request.url
        url = self.request.current_route_url()
        came_from = request.params.get('came_from', referrer)
        login = ''
        password = ''
        error = ''

        if 'form.submitted' in request.POST:
            login = request.POST['login']
            password = request.POST['password']
            connector = get_ldap_connector(request)

            data = connector.authenticate(login, password)

            if data is not None:
                dn = data[0]
                headers = remember(request, dn)
                return HTTPFound(location=came_from, headers=headers)
            error = 'Invalid credentials'

        return dict(
            login_url=url,
            came_from=came_from,
            login=login,
            password=password,
            error=error)


def _update_req(appstruct, request):
    reqsettings = request.registry.settings
    slt = reqsettings['unid_salt']
    hashids = Hashids(salt=slt)
    unid = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    ai = appstruct.items()
    ai = dict(ai)
    sess = DBSession()

    # now = now.strftime('%y%m%d%H%M%S')
    now = datetime.now()
    unid = hashids.encode(int(unid))
    givenName = ai['givenName']
    middleName = ai['middleName']
    sn = ai['sn']
    suffix = ai['suffix']
    cn = ai['cn']
    street = ai['street']
    lcity = ai['lcity']
    st = ai['st']
    postalCode = ai['postalCode']
    country = ai['country']
    mail = ai['mail']
    mailPreferred = ai['mailPreferred']
    phone = ai['phone']
    cell = ai['cell']
    employerType = ai['employerType']
    employerName = ai['employerName']
    citizenStatus = ai['citizenStatus']
    citizenships = [sess.query(CountryCodes
                    ).filter(CountryCodes.code == i).one()
                    for i in ai['citizenships']]
    birthCountry = ai['birthCountry']
    nrelUserID = ai['nrelUserID']
    preferredUID = ai['preferredUID']
    justification = ai['justification']
    comments = ai['comments']
    couTimestamp = now
    storTimestamp = now
    subTimestamp = now

    if not cn:
        cn = "%s, %s" % (givenName, sn)

    submission = Request(
        unid=unid,
        givenName=givenName,
        middleName=middleName,
        sn=sn,
        suffix=suffix,
        cn=cn,
        street=street,
        lcity=lcity,
        st=st,
        postalCode=postalCode,
        country=country,
        mail=mail,
        mailPreferred=mailPreferred,
        phone=phone,
        cell=cell,
        employerType=employerType,
        employerName=employerName,
        citizenStatus=citizenStatus,
        citizenships=citizenships,
        birthCountry=birthCountry,
        nrelUserID=nrelUserID,
        preferredUID=preferredUID,
        justification=justification,
        comments=comments,
        subTimestamp=subTimestamp,
        couTimestamp=couTimestamp,
        storTimestamp=storTimestamp
        )

    # write the data
    DBSession().add(submission)
    transaction.commit()
    # return the unid for processing in next form
    return str(unid)

