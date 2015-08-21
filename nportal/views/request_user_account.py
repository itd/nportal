import datetime
# from pyramid.response import Response
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config
from pyramid.renderers import get_renderer
# from sqlalchemy.exc import DBAPIError

import deform
import deform.widget
from deform import (widget)  # decorator, default_renderer, field, form,
import colander

from nportal.models import (
    DBSession,
    UserAccountModel
)

from nportal.views import strip_whitespace, remove_multiple_spaces
from .lists import (us_states, country_codes)


@colander.deferred
def deferred_country_widget(node, kw):
    country_codes_data = kw.get('country_codes_data', [])
    return widget.SelectWidget(values=country_codes_data)

def deferred_state_widget(node, kw):
    us_states_data = kw.get('us_states_data', [])
    return widget.SelectWidget(values=us_states_data)

class AddAccountSchema(colander.MappingSchema):
    page_title = colander.SchemaNode(colander.String())
    body = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
    )

    cn = colander.SchemaNode(
        colander.String(),
        title='Common or Nick Name',
        description='Your full name. How you want to be addressed.',
        validator=colander.Length(min=2, max=64),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='cn'
    )

    givenName = colander.SchemaNode(
        colander.String(),
        title='First Name/Given Name',
        description='Your legal First Name.',
        validator=colander.Length(min=1, max=64),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='givenName'
    )

    sn = colander.SchemaNode(
        colander.String(),
        title='Last Name',
        description='Your legal family name or last name.',
        validator=colander.Length(min=1, max=64),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='sn'
    )

    middleName = colander.SchemaNode(
        colander.String(),
        title='Middle Name',
        description='Your legal middle name if applicable.',
        validator=colander.Length(min=0, max=64),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='middleName'
    )

    suffix = colander.SchemaNode(
        colander.String(),
        title='Suffix',
        description='(Sr. Jr. IV, etc.)',
        validator=colander.Length(min=0, max=32),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='suffix'
    )

    userTitle = colander.SchemaNode(
        colander.String(),
        title='Title',
        description='A title you may currently use',
        validator=colander.Length(min=0, max=128),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='userTitle'
    )

    street = colander.SchemaNode(
        colander.String(),
        title='Street Address',
        description='',
        validator=colander.Length(min=0, max=400),
        widget=widget.TextAreaWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='street'
    )

    l = colander.SchemaNode(
        colander.String(),
        title='City',
        description='',
        validator=colander.Length(min=1, max=128),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='l'
    )

    st = colander.SchemaNode(
        colander.String(),
        title='State / Province / Region',
        description='',
        validator=colander.Length(min=1, max=128),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='l'
    )

    postalCode = colander.SchemaNode(
        colander.String(),
        title='Post Code / ZIP Code',
        description='',
        validator=colander.Length(min=0, max=64),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='postalCode'
    )

    country = colander.SchemaNode(
        colander.String(),
        title='Country',
        description='',
        validator=colander.Length(min=0, max=64),
        widget=deferred_country_widget,
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='country'
    )

    #   mail

    #   phone

    #   cell

    #   employerType

    #   employerSponsor

    #   employerSponsorName

    #   shipAddrSame

    #   shipAddr

    #   shipAddr2

    #   shipAddrCity

    #   shipAddrState

    #   shipAddrPostCode

    #   shipAddrCountry

    #   position

    #   positionDesc

    #   citizen

    #   citizenOf

    #   birthCountry

    #   projectPI

    #   projectID

    #   projectWorkDesc

    #   projPublishable

    #   projProprietary

    #   projRestricted

    #   nrelPreviousAccount

    #   nrelExistingAccount

    #   nrelExistingUserID

    #   nrelUserID

    #   preferredUID

    #   comments = colander.SchemaNode(
    #       colander.String(),
    #       widget=deform.widget.RichTextWidget()
    #   )

    #   subTimestamp

    #   couTimestamp

    cou = colander.SchemaNode(
        colander.Boolean(),
        title='COU Acceptance',
        description='Check this if you have read and agree '
                    'to the cyber security policies.',
        widget=deform.widget.CheckboxWidget(),
        oid='cou'
    )

    #   storTimestamp
    stor = colander.SchemaNode(
        colander.Boolean(),
        title='Storage Acceptance',
        description='Check this if you have read and agree '
                    'to the Center\'s storage policies.',
        widget=deform.widget.CheckboxWidget(),
        oid='stor'
    )
    #   cybeTimestamp
    cyber = colander.SchemaNode(
        colander.Boolean(),
        title='Cyber Security Policy Acceptance',
        description='Check this if you have read and agree to abide by '
                    'the Center\'s Cyber Security policies.',
        widget=deform.widget.CheckboxWidget(),
        oid='stor'
    )


class AccountRequestView(object):
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("../templates/_layout.pt")
        self.layout = renderer.implementation().macros['layout']
        self.title = "Account Request Form"
    def render_form(self, form, appstruct=colander.null,
                    submitted='submit',
                    success=None, readonly=False):
        captured = None
        if submitted in self.request.POST:
            # the request represents a form submission
            controls = self.request.POST.items()
            try:
                # try to validate the submitted values
                captured = form.validate(controls)
                if success:
                    response = success()
                    if response is not None:
                        return response
                self.title = 'Form data accepted'
                # set this to redir to /allloc/view/<allocid>
                _add_new_user_request(captured)

            except deform.ValidationFailure as e:
                # the submitted values could not be validated
                html = e.render()
                return dict(form=html, captured=repr(captured),
                            title=self.title)

            # Data should be added by now.
            # Send the user's browser to the detailed view.
            view_url = self.request.route_url('request_received_view',
                                              fname=captured['fname'])
            return HTTPFound(view_url)
        else:
            # the request requires a simple form rendering
            html = form.render(appstruct=appstruct)
            # values passed to template for rendering
            return dict(form=html,
                        captured=repr(captured),
                        title=self.title,
                        # logged_in=authenticated_userid(self.request)
                        )

    @reify
    def account_req_form(self):

        # import pdb; pdb.set_trace()

        schema = AddAccountSchema().bind(
            country_codes_data=country_codes,
            us_states_data=us_states
        )
        return deform.Form(schema, buttons=('submit',))

    @reify
    def reqts(self):
        return self.account_req_form.get_widget_resources()

    @view_config(route_name='request_received_view',
                 renderer='../templates/request_received.pt')
    def request_received_view(self):
        return {'title': 'request received',
                'page_title': 'Account request submission received'}


    @view_config(route_name='request_user_account',
                 renderer='../templates/request_user_account.pt')
    def add_new_user_account(self):
        schema = AddAccountSchema().bind(
            country_codes_data=country_codes,
            us_states_data=us_states,
        )
        form = deform.Form(schema,
                           buttons=('submit',),
                           # action=self.request.route_url('allocation_add')
                           )
        return self.render_form(form)


def _add_new_user_request(appstruct):
    ai = appstruct.items()
    ai = dict(ai)

    now = datetime.datetime.now()
    cou = None
    stor = None
    cyber = None
    if ai['cou']:
        cou = now
    if ai['stor']:
        stor = now
    if ai['cyber']:
        cyber = now

    # now = now.strftime('%y%m%d%H%M%S')
    # pi = [sess.query(Users).filter(Users.pi == i) for i in ai['users']]
    users = [DBSession().query(UserAccountModel
                               ).filter(UserAccountModel.userid == i).one()
             for i in ai['users']]

    # q1 = q2 = q3 = q4 = None
    # if ai['q1']:
    #     q1 = int(ai['q1'])
    # if ai['q2']:
    #     q2 = int(ai['q2'])
    # if ai['q3']:
    #     q3 = int(ai['q3'])
    # if ai['q4']:
    #     q4 = int(ai['q4'])
    # q1 = [None, int(ai['q1'])][ai['q1']]
    # q2 = [None, int(ai['q2'])][ai['q2']]
    # q3 = [None, int(ai['q3'])][ai['q3']]
    # q4 = [None, int(ai['q4'])][ai['q4']]
    # q2 = int(ai['q2']),
    # q3 = int(ai['q3']),
    # q4 = int(ai['q4'])

    submission = UserAccountModel(
        cn=ai['allocid'],
        givenName=ai['handleid'],
        sn=ai['pi'],
        middleName=ai['system'],
        suffix=users,
        userTitle=ai['nodehours'],
        street=ai['pspace'],
        l=ai['mspace'],
        st=ai['adgroup'],
        postalCode=ai['startdate'],
        country=ai['enddate'],
        subTimestamp=now,
        couTimestamp=cou,
        storTimestamp=stor,
        cyberTimestamp=cyber,
    )

    # storagegrp=ai['storagegrp'],
    DBSession().add(submission)
