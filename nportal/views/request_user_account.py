import datetime
import string

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
import htmllaundry
from htmllaundry import sanitize

from nportal.models import (
    DBSession,
    UserAccountModel
    )

from nportal.views import (strip_whitespace,
                           remove_multiple_spaces,
                           rm_spaces
                           )

from .lists import (us_states,
                    country_codes,
                    true_false,
                    employment_positions,
                    title_prefixes,
                    citizen_types)


def phone_validator(node, value):
    """ checks to make sure that the value looks like a phone number """
    allowed = set(string.ascii_lowercase + string.digits +
                  ' ' + '.' + '+' + '(' + ')' + '-')
    tval = set(value) <= allowed

    if not tval:
        raise colander.Invalid(node,
               '%r is not a valid telephone number format' % value)


def cyber_validator(node, value):
    if not value:
        raise colander.Invalid(node, 'You must agree to the Cyber Policies')


def cou_validator(node, value):
    if not value:
        raise colander.Invalid(node,
            'You must agree to the Conditions of Use Policies')


def stor_validator(node, value):
    if not value:
        raise colander.Invalid(node,
                               'You must agree to the HPC Storage Policies')


@colander.deferred
def deferred_country_widget(node, kw):
    country_codes_data = kw.get('country_codes_data', [])
    return widget.SelectWidget(values=country_codes_data)

def deferred_state_widget(node, kw):
    us_states_data = kw.get('us_states_data', [])
    return widget.SelectWidget(values=us_states_data)

email_confirm_widget = deform.widget.CheckedInputWidget(
            subject='Email',
            confirm_subject='Confirm Email',
            )


class AddAccountSchema(colander.MappingSchema):
    page_title = colander.SchemaNode(colander.String())
    body = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
    )

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
        validator=cyber_validator,
        oid='stor'
    )

    titlePrefix = colander.SchemaNode(
        colander.String(),
        title='Title/Prefix',
        description='Your full name. How you want to be addressed.',
        validator=colander.Length(min=2, max=64),
        widget=widget.SelectWidget(value=title_prefixes),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='titlePrefix'
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
        validator=colander.Length(min=0, max=200),
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

    mail = colander.SchemaNode(
        colander.String(),
        title='EMail',
        description='Your primary email account',
        validator=colander.Email(msg="Please provide a valid Email address"),
        preparer=[rm_spaces, htmllaundry.sanitize],
        widget=email_confirm_widget,
        oid='mail'
    )
    phone = colander.SchemaNode(
        colander.String(),
        title='Telephone',
        description='Please provide your primary telephone number',
        preparer=[strip_whitespace, remove_multiple_spaces],
        validator=phone_validator,
        oid='phone'
    )

    cell = colander.SchemaNode(
        colander.String(),
        title='Cell',
        description='We will use your cell phone number for verification',
        validator=phone_validator,
        #widget=,
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='cell'
    )

    employerType = colander.SchemaNode(
        colander.String(),
        title='Employer Type',
        description='',
        validator=colander.Length(min=0, max=64),
        #widget=,
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='employerType'
    )

    # employerSponsor = colander.SchemaNode(
    #     colander.Boolean(),
    #     title='Employment/Institution supporting this work',
    #     description='click if the same as employer above',
    #     widget=widget.CheckboxWidget(),
    #     oid='employerSponsor'
    # )
    #
    # employerSponsorName = colander.SchemaNode(
    #     colander.String(),
    #     title='Sponsor Name',
    #     description='''If the name of the sponsor is not
    #                 listed above, please list it here''',
    #     validator=colander.Length(min=0, max=128),
    #     widget=widget.TextInputWidget(),
    #     missing=unicode(''),
    #     preparer=[strip_whitespace, remove_multiple_spaces],
    #     oid='employerSponsorName'
    # )

    shipAddrSame = colander.SchemaNode(
        colander.Bool(),
        title='Shipping Address',
        description='click if this is the same as above',
        widget=widget.CheckboxWidget(),
        oid='shipAddrSame'
    )

    shipAddr = colander.SchemaNode(
        colander.String(),
        missing=None,
        title='Address',
        description='Your shipping address - in case we need to send you a physical VPN token.',
        validator=colander.Length(min=0, max=128),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, htmllaundry.sanitize],
        oid='shipAddr'
    )


    shipAddrCity = colander.SchemaNode(
        colander.String(),
        title='City',
        description='',
        validator=colander.Length(min=0, max=128),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        oid='shipAddrCity'
    )

    shipAddrState = colander.SchemaNode(
        colander.String(),
        title='State / Province / Region',
        description='',
        validator=colander.Length(min=0, max=64),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces, sanitize],
        oid='shipAddrCity'
    )

    shipAddrPostCode = colander.SchemaNode(
        colander.String(),
        title='Postal Code / Zip',
        description='',
        validator=colander.Length(min=0, max=64),
        widget=widget.TextInputWidget(),
        preparer=[htmllaundry.sanitize],
        oid='shipAddr'
    )

    shipAddrCountry = colander.SchemaNode(
        colander.String(),
        title='',
        description='',
        validator=colander.Length(min=0, max=64),
        widget=deferred_country_widget,
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='shipAddrCountry',
    )
    #
    # position = colander.SchemaNode(
    #     colander.String(),
    #     title='Position',
    #     description='What is your position or job with this institution?',
    #     validator=colander.OneOf([x[0] for x in employment_positions]),
    #     widget=deform.widget.RadioChoiceWidget(values=employment_positions),
    #     oid='position'
    # )
    #
    # positionDesc = colander.SchemaNode(
    #     colander.String(),
    #     title='Position Description',
    #     description='if other, please describe your position',
    #     validator=colander.Length(min=0, max=64),
    #     widget=widget.TextInputWidget(),
    #     preparer=[strip_whitespace, sanitize],
    #     oid='positionDesc'
    # )

    citizenStatus = colander.SchemaNode(
        colander.Boolean(),
        title='Citizenship Status',
        description='Select the option that is most true for you',
        validator=colander.OneOf([x[0] for x in citizen_types]),
        widget=deform.widget.RadioChoiceWidget(values=citizen_types),
        oid='citizenStatus'
    )

    # citizenType = colander.SchemaNode(
    #     colander.Boolean(),
    #     title='multiCitizen',
    #     description='I have multiple Citizenships',
    #     widget=deform.widget.RadioChoiceWidget(values=citizen_types),
    #     oid='citizen'
    # )

    citizenOf = colander.SchemaNode(
        colander.String(),
        title='Citizen of',
        description='If you one or more citizenships, '
                    'please select them from the list',
        validator=colander.ContainsOnly([x[0] for x in citizen_types]),
        widget=deferred_country_widget,
        oid='citizenOf',
    )

    #   birthCountry

    nrelExistingAccount = colander.SchemaNode(
        colander.Boolean(),
        title='NREL Account',
        description='If you have, or have previously used, an '
                    'NREL HPC account, check this.',
        widget=deform.widget.CheckboxWidget(),
        oid='nrelExistingAccount'
    )

    nrelUserID = colander.SchemaNode(
        colander.String(),
        title='NREL UserID',
        description='If you have --or have previously used-- an NREL userid, '
                    'please enter it here.',
        validator=colander.Length(min=1, max=16),
        widget=widget.TextInputWidget(),
        preparer=[htmllaundry.sanitize],
        oid='nrelUserID'
    )

    #   preferredUID
    preferredUID = colander.SchemaNode(
        colander.String(),
        title='Preferred UserID',
        description="If you've never had an NREL account or userid, please "
                    "tell us what you'd like to use for a login userID.",
        validator=colander.Length(min=1, max=16),
        widget=widget.TextInputWidget(),
        preparer=[htmllaundry.sanitize],
        oid='preferredUID'
    )

    comments = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(rows=6, columns=60),
        preparer=[htmllaundry.sanitize],
        validator=colander.Length(max=1000),
        oid='comments'
    )

    #   subTimestamp
    #   couTimestamp
    #   storTimestamp
    #   cyberTimestamp


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

    submission = UserAccountModel(
        cn=ai['allocid'],
        titlePrefix=ai['titlePrefix'],
        givenName=ai['handleid'],
        sn=ai['pi'],
        middleName=ai['system'],
        suffix=ai['suffix'],

        userTitle=ai['nodehours'],
        street=ai['pspace'],
        l=ai['mspace'],
        st=ai['adgroup'],
        postalCode=ai['postalCode'],
        country=ai['country'],
        mail=ai['mail'],
        mailPreferred=ai['mailPreferred'],
        phone=ai['phone'],
        cell=ai['cell'],
        phonePrimary=ai['phonePrimary'],
        employerType=ai['employerType'],
        employerName=ai['employerName'],
        employerAddress=ai['employerAddress'],
        shipAddrSame=ai['shipAddrSame'],
        shipAddr=ai['shipAddr'],
        citizenStatus=ai['citizenStatus'],
        citizenOf=ai['citizenOf'],
        nrelExistingAccount=ai['nrelExistingAccount'],
        nrelUserID=ai['nrelUserID'],
        preferredUID=ai['preferredUID'],
        comments=ai['comments'],
        subTimestamp=now,
        couTimestamp=cou,
        storTimestamp=stor,
        cyberTimestamp=cyber,
    )

    # storagegrp=ai['storagegrp'],
    DBSession().add(submission)

