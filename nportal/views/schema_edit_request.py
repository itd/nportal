import deform
import deform.widget
from deform import (widget)  # decorator, default_renderer, field, form,
import colander

# import htmllaundry
# from htmllaundry import sanitize

from validators import (cyber_validator,
                        phone_validator,
                        stor_validator,
                        cou_validator,
                        valid_country,
                        valid_countries)

from .lists import (title_prefixes,
                    citizen_types,
                    employer_types,
                    country_codes,
                    has_account,
                    approval_status
                    )


@colander.deferred
def deferred_country_widget(node, kw):
    country_codes_data = kw.get('country_codes_data', [])
    return widget.Select2Widget(values=country_codes_data)


@colander.deferred
def deferred_state_widget(node, kw):
    us_states_data = kw.get('us_states_data', [])
    return widget.Select2Widget(values=us_states_data)


@colander.deferred
def deferred_title_prefix_widget(node, kw):
    title_prefix_data = kw.get('title_prefix_data', [])
    return widget.Select2Widget(values=title_prefix_data)


@colander.deferred
def deferred_review_status_widget(node, kw):
    return deform.widget.RadioChoiceWidget(values=approval_status)


@colander.deferred
def deferred_review_status_validator(node, kw):
    return colander.OneOf([x[0] for x in approval_status])


# email_confirm_widget = deform.widget.CheckedInputWidget(
#             subject='Email address',
#             confirm_subject='Confirm your Email address',
#             )
#
# pref_email_confirm_widget = deform.widget.CheckedInputWidget(
#             subject='Optional Preferred Email',
#             confirm_subject='Confirm your optional Email address',
#             )

sn_widget = widget.TextInputWidget(css_class='form-control')


class EditRequestSchema(colander.Schema):
    # couTimestamp
    cou = colander.SchemaNode(
        colander.Boolean(),
        title='COU Policy Acceptance',
        description='Terms and Conditions Agreement - Check this if '
                    'you have read and agree to the cyber security policies.',
        widget=widget.TextInputWidget(),
        oid='cou'
        )

    #   storTimestamp
    stor = colander.SchemaNode(
        colander.Boolean(),
        title='Data Security Policy Acceptance',
        description='Check this if you have read and agree '
                    'to the Center\'s storage policies.',
        widget=widget.HiddenWidget(),
        validator=stor_validator,
        oid='stor'
    )
    #   cybeTimestamp
    # cyber = colander.SchemaNode(
    #     colander.Boolean(),
    #     title='Cyber Security Policy Acceptance',
    #     description='Check this if you have read and agree to abide by '
    #                 'the Center\'s Cyber Security policies.',
    #     widget=deform.widget.CheckboxWidget(),
    #     validator=cyber_validator,
    #     oid='cyber'
    # )

    # titlePrefix = colander.SchemaNode(
    #     colander.String(),
    #     title='Honorary',
    #     description='If you prefer to use n honorary, enter it here.',
    #     # validator=colander.ContainsOnly([x[0] for x in title_prefixes]),
    #     #validator=colander.Length(min=1, max=64),
    #     widget=widget.TextInputWidget(placeholder="Dr., Mr., Ms., etc."),
    #     missing=unicode(''),
    #     oid='titlePrefix'
    # )

    givenName = colander.SchemaNode(
        colander.String(),
        title='Given/First name',
        description='Your given or first name',
        validator=colander.Length(min=1, max=64),
        widget=widget.HiddenWidget(),
        oid='givenName'
    )

    middleName = colander.SchemaNode(
        colander.String(),
        title='Middle name/initial',
        description='Middle name or initial',
        validator=colander.Length(min=0, max=64),
        widget=widget.HiddenWidget(),
        missing=unicode(''),
        oid='middleName'
    )

    sn = colander.SchemaNode(
        colander.String(),
        title='Family/Last Name',
        description='family Name / Last Name',
        validator=colander.Length(min=1, max=64),
        widget=widget.HiddenWidget(),
        oid='sn'
    )

    suffix = colander.SchemaNode(
        colander.String(),
        title='Suffix',
        description='(Sr. Jr. IV, etc.)',
        validator=colander.Length(min=0, max=32),
        widget=widget.HiddenWidget(),
        missing=unicode(''),
        oid='suffix'
    )

    cn = colander.SchemaNode(
        colander.String(),
        title='Common or Nick Name',
        description='Your full name. How you want to be addressed.',
        validator=colander.Length(min=3, max=64),
        widget=widget.HiddenWidget(),
        missing=unicode(''),
        oid='cn'
    )

    street = colander.SchemaNode(
        colander.String(),
        title='Street Address',
        description='',
        validator=colander.Length(min=0, max=200),
        widget=widget.HiddenWidget(),
        oid='street'
    )

    lcity = colander.SchemaNode(
        colander.String(),
        title='City',
        description='',
        validator=colander.Length(min=1, max=128),
        widget=widget.HiddenWidget(),
        oid='lcity'
    )

    st = colander.SchemaNode(
        colander.String(),
        title='State/Province',
        description='',
        validator=colander.Length(min=1, max=128),
        widget=widget.HiddenWidget(),
        oid='l'
    )

    postalCode = colander.SchemaNode(
        colander.String(),
        title='Post/ZIP Code',
        description='',
        validator=colander.Length(min=2, max=64),
        widget=widget.HiddenWidget(),
        oid='postalCode'
    )

    country = colander.SchemaNode(
        colander.String(),
        title='Country',
        description='',
        widget=widget.HiddenWidget(),
        validator=valid_country,
        oid='country'
    )

    mail = colander.SchemaNode(
        colander.String(),
        title='EMail',
        description='Your primary email account',
        widget=widget.HiddenWidget(),
        oid='mail'
    )
    #
    # mailPreferred = colander.SchemaNode(
    #     colander.String(),
    #     title='Preferred EMail',
    #     description='optional preferred email account',
    #     missing=unicode(''),
    #     widget=widget.TextInputWidget(),
    #     oid='mail'
    # )

    phone = colander.SchemaNode(
        colander.String(),
        title='Phone number',
        description='Please provide your primary telephone number',
        validator=phone_validator,
        widget=widget.HiddenWidget(),
        oid='phone'
    )

    cell = colander.SchemaNode(
        colander.String(),
        title='Cell phone number',
        description='For contact and verification',
        validator=phone_validator,
        missing=unicode(''),
        #widget=widget.TextInputWidget(),
        widget=widget.HiddenWidget(),
        oid='cell'
    )

    employerType = colander.SchemaNode(
        colander.String(),
        # validator=colander.OneOf([x[0] for x in employer_types]),
        widget=widget.HiddenWidget(),
        title='Employer Type',
        description='Select the employer type from the list below that '
                    'is most appropriate to your request',
        oid="employerType"
    )

    employerName = colander.SchemaNode(
        colander.String(),
        title='Employer/Institution/Sponsor',
        description='Provided employer or institution name',
        validator=colander.Length(min=3, max=128),
        widget=widget.HiddenWidget(),
        oid='employerName'
    )

    citizenStatus = colander.SchemaNode(
        colander.String(),
        title='Citizenship Status',
        description='Select one of the following options '
                    'that best describes your U.S. citizenship status',
        validator=colander.OneOf([x[0] for x in citizen_types]),
        widget=widget.HiddenWidget(),
        oid='citizenStatus'
    )

    citizenships = colander.SchemaNode(
        colander.Set(),
        title='Citizenships',
        description='Please select your country or countries of citizenship',
        validator=valid_countries,
        widget=widget.HiddenWidget(),
        oid='citizenships',
    )

    birthCountry = colander.SchemaNode(
        colander.String(),
        title='Country of birth',
        description='Please enter/select your country of birth',
        validator=valid_country,
        widget=widget.HiddenWidget(),
        oid='birthCountry',
    )

    nrelUserID = colander.SchemaNode(
        colander.String(),
        title='Your Existing NREL HPC UserID',
        description='If you have --or previously had-- an NREL UserID, '
                    'enter it here.',
        validator=colander.Length(min=1, max=16),
        widget=widget.TextInputWidget(),
        missing=unicode(''),
        oid='nrelUserID'
    )

    justification = colander.SchemaNode(
        colander.String(),
        title='Justification',
        widget=widget.HiddenWidget(),
        missing=unicode(''),
        validator=colander.Length(max=1000),
        description="If you don't have an account on NREL HPC systems, "
                    "we need some additional information. Please provide "
                    "the project handles or titles of the project allocations "
                    "you are associated with. "
                    "If you don't have an allocation, please tell us "
                    "why you are requesting NREL HPC login credentials.",
        oid='comments'
    )

    preferredUID = colander.SchemaNode(
        colander.String(),
        title='*New* ESIF HPC UserID',
        description="Please provide your desired User ID here.<sup>1</sup>"
                    "(3 to 16 characters, all lower case.)",
        validator=colander.Length(min=3, max=16),
        widget=widget.TextInputWidget(),
        missing=unicode(''),
        oid='preferredUID'
    )

    comments = colander.SchemaNode(
        colander.String(),
        title='Additional Notes or Comments',
        widget=widget.HiddenWidget(),
        missing=unicode(''),
        validator=colander.Length(max=1000),
        description='If you think we need any additional '
                'information to process or approve your request, '
                'please let us know.',
        oid='comments'
    )

    UserID = colander.SchemaNode(
        colander.String(),
        title='Assigned UserID',
        description='Determined by Center Operations.'
                    ' This MUST match what is in IDM.',
        validator=colander.Length(min=1, max=16),
        widget=widget.TextInputWidget(),
        missing=unicode(''),
        oid='UserID'
    )

    approvalStatus = colander.SchemaNode(
        colander.Integer(),
        title='Approval Status',
        description='The current status of the request\'s review process',
        validator=colander.OneOf([x[0] for x in approval_status]),
        default=0,
        widget=widget.RadioChoiceWidget(values=approval_status),
        oid='approvalStatus'
    )


    #   subTimestamp
    #   couTimestamp
    #   storTimestamp
    #   cyberTimestamp
