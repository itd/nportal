import os
import datetime
import string

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import (scoped_session, sessionmaker)

# from pyramid.response import Response
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound

from pyramid.session import SignedCookieSessionFactory
from pyramid.config import Configurator

from pyramid.view import view_config
from pyramid.renderers import get_renderer
# from sqlalchemy.exc import DBAPIError
#import deform
from deform import (ZPTRendererFactory,
                    Form,
                    widget,
                    ValidationFailure)
    # decorator, default_renderer, field, form,
import colander
from pkg_resources import resource_filename

from nportal.models import (
    DBSession,
    UserAccountModel
    )

from schemas import AddAccountSchema

from .lists import (us_states,
                    country_codes,
                    title_prefixes,
                    cou_policy,
                    stor_policy,
                    cyber_policy)

# sqlalchemy setup
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),
                                        expire_on_commit=False))
sess = DBSession()

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
    renderer = get_renderer("../templates/_layout.pt")
    layout = renderer.implementation().macros['layout']
    return layout


class AccountRequestView(object):
    """
    """
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("../templates/_layout.pt")
        #self.layout = renderer.implementation().macros['layout']
        self.layout = site_layout()
        self.title = "Account Request Form"

    @reify
    def account_req_form(self):
        schema = AddAccountSchema().bind(
            country_codes_data=country_codes,
            us_states_data=us_states
        )
        return Form(schema, buttons=('submit',))

    @reify
    def reqts(self, request):
        return self.account_req_form.get_widget_resources()

    @view_config(route_name='request_user_account',
                 renderer='../templates/request_user_account.pt')
    def add_new_user_account(self):
        ###

        ###
        # instantiate our colander schema
        schema = AddAccountSchema().bind(
            country_codes_data=country_codes,
            us_states_data=us_states,
            title_prefix_data=title_prefixes,
        )
        request = self.request
        session = request.session
        Form.set_zpt_renderer(search_path)

        # see if a user submitted the form
        submitted = 'submit' in request.POST

        # get the user email from the POST request, if present
        user_email = request.POST.get('email', '')

        # get the form control field names and values as a list of tuples
        controls = request.POST.items()


        # create a deform form object from the schema
        # form = deform.Form(schema)

        form = Form(schema,
                    action=request.route_url('request_user_account'),
                    form_id='deformRegform'
                    )

        if submitted:
            # it's a submission, process it
            controls = self.request.POST.items()
            captured = None
            try:
                # try to validate the submitted values
                captured = form.validate(controls)
                request.session.flash("It submitted! (not really)")
                _add_new_user_request(captured, request)
                # Send the user's browser to the detailed view.

                #return HTTPFound(location=view_page)

                # title="Success!!!",
                # givenName=request.POST['givenName']
                view_url = request.route_url('request_received_view',
                                              givenName=controls['givenName'])
                return HTTPFound(view_url)

            except ValidationFailure as e:
                # the submitted values could not be validated
                return dict(form=form)

        else:
            # not submitted, render form
            return dict(form=form)


    @view_config(route_name='request_received_view',
                 renderer='../templates/request_received.pt')
    def request_received_view(self):
        import pdb; pdb.set_trace()
        return dict(title='Account request submission received')
        # givenName: self.request.POST['givenName']


def _add_new_user_request(appstruct, request):
    ai = appstruct.items()
    ai = dict(ai)

    now = datetime.datetime.now()
    cou = None
    stor = None
    cyber = None
    if ai['cou']:
        couTimestamp = now
    if ai['stor']:
        storTimestamp = now
    if ai['cyber']:
        cyberTimestamp = now

    # now = now.strftime('%y%m%d%H%M%S')

    submission = UserAccountModel(
        titlePrefix=ai['titlePrefix'],
        givenName=ai['givenName'],
        middleName=ai['middleName'],
        sn=ai['sn'],
        suffix=ai['suffix'],
        cn=ai['cn'],

        # userTitle=ai['userTitle'],
        # street=ai['street'],
        # l=ai['l'],
        # st=ai['st'],
        # postalCode=ai['postalCode'],
        # country=ai['country'],
        # mail=ai['mail'],
        # mailPreferred=ai['mailPreferred'],
        # phone=ai['phone'],
        # cell=ai['cell'],
        # phonePrimary=ai['phonePrimary'],
        # employerType=ai['employerType'],
        # employerName=ai['employerName'],
        # employerAddress=ai['employerAddress'],
        # shipAddrSame=ai['shipAddrSame'],
        # shipAddr=ai['shipAddr'],
        # citizenStatus=ai['citizenStatus'],
        # citizenOf=ai['citizenOf'],
        # nrelExistingAccount=ai['nrelExistingAccount'],
        # nrelUserID=ai['nrelUserID'],
        # preferredUID=ai['preferredUID'],
        # comments=ai['comments'],

        subTimestamp=now,
        couTimestamp=couTimestamp,
        storTimestamp=storTimestamp,
        cyberTimestamp=cyberTimestamp
        )

    # storagegrp=ai['storagegrp'],
    DBSession().add(submission)
