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


email_confirm_widget = deform.widget.CheckedInputWidget(
            subject='Email address',
            confirm_subject='Confirm your Email address',
            )

pref_email_confirm_widget = deform.widget.CheckedInputWidget(
            subject='Optional Preferred Email',
            confirm_subject='Confirm your optional Email address',
            )

sn_widget = widget.TextInputWidget(
            css_class='form-control')


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
        widget=deform.widget.CheckboxWidget(),
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
        widget=widget.TextInputWidget(),
        oid='givenName'
    )

    middleName = colander.SchemaNode(
        colander.String(),
        title='Middle name/initial',
        description='Middle name or initial',
        validator=colander.Length(min=0, max=64),
        widget=widget.TextInputWidget(),
        missing=unicode(''),
        oid='middleName'
    )

    sn = colander.SchemaNode(
        colander.String(),
        title='Family/Last Name',
        description='family Name / Last Name',
        validator=colander.Length(min=1, max=64),
        widget=widget.TextInputWidget(
            placeholder=''),
        oid='sn'
    )

    suffix = colander.SchemaNode(
        colander.String(),
        title='Suffix',
        description='(Sr. Jr. IV, etc.)',
        validator=colander.Length(min=0, max=32),
        widget=widget.TextInputWidget(placeholder='example: III, PhD, etc.'),
        missing=unicode(''),
        oid='suffix'
    )

    cn = colander.SchemaNode(
        colander.String(),
        title='Common or Nick Name',
        description='Your full name. How you want to be addressed.',
        validator=colander.Length(min=3, max=64),
        widget=widget.TextInputWidget(
        placeholder='(Optional) How you want to be addressed '
                    'if different from: FirstName LastName'),
        missing=unicode(''),
        oid='cn'
    )

    street = colander.SchemaNode(
        colander.String(),
        title='Street Address',
        description='',
        validator=colander.Length(min=0, max=200),
        widget=widget.TextInputWidget(placeholder='example: 123 Noe Way'),
        oid='street'
    )

    lcity = colander.SchemaNode(
        colander.String(),
        title='City',
        description='',
        validator=colander.Length(min=1, max=128),
        widget=widget.TextInputWidget(),
        oid='lcity'
    )

    st = colander.SchemaNode(
        colander.String(),
        title='State/Province',
        description='',
        validator=colander.Length(min=1, max=128),
        widget=widget.TextInputWidget(),
        oid='l'
    )

    postalCode = colander.SchemaNode(
        colander.String(),
        title='Post/ZIP Code',
        description='',
        validator=colander.Length(min=2, max=64),
        widget=widget.TextInputWidget(),
        oid='postalCode'
    )

    country = colander.SchemaNode(
        colander.String(),
        title='Country',
        description='',
        widget=widget.SelectWidget(values=country_codes),
        #validator=colander.OneOf([x[0] for x in country_codes]),
        validator=valid_country,
        oid='country'
    )

    mail = colander.SchemaNode(
        colander.String(),
        title='EMail',
        description='Your primary email account',
        # validator=colander.Email(msg="Please provide your work Email address. This will be the primary account we use to contact you."),
        widget=widget.TextInputWidget(),
        oid='mail'
    )

    mailPreferred = colander.SchemaNode(
        colander.String(),
        title='Preferred EMail',
        description='optional preferred email account',
        missing=unicode(''),
        widget=widget.TextInputWidget(),
        oid='mail'
    )

    phone = colander.SchemaNode(
        colander.String(),
        title='Phone number',
        description='Please provide your primary telephone number',
        validator=phone_validator,
        widget=widget.TextInputWidget(),
        oid='phone'
    )

    cell = colander.SchemaNode(
        colander.String(),
        title='Cell phone number',
        description='For contact and verification',
        validator=phone_validator,
        missing=unicode(''),
        widget=widget.TextInputWidget(
        placeholder='(Optional) example: +1-000-000-0000'),
        oid='cell'
    )

    employerType = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf([x[0] for x in employer_types]),
        widget=deform.widget.RadioChoiceWidget(values=employer_types),
        title='Employer Type',
        description='Select the employer type from the list below that '
        'is most appropriate to your request',
        oid="employerType"
    )

    employerName = colander.SchemaNode(
        colander.String(),
        title='Employer, Institution, or Sponsor Name',
        description='Please provide the name of your employer or '
                    'the institution you represent',
        validator=colander.Length(min=3, max=128),
        widget=widget.TextInputWidget(placeholder='employer name here'),
        oid='employerName'
    )

    citizenStatus = colander.SchemaNode(
        colander.String(),
        title='Citizenship Status',
        description='Select one of the following options '
            'that best describes your U.S. citizenship status',
        validator=colander.OneOf([x[0] for x in citizen_types]),
        widget=deform.widget.RadioChoiceWidget(values=citizen_types),
        oid='citizenStatus'
    )

    citizenships = colander.SchemaNode(
        colander.Set(),
        title='Citizenships',
        description='Please select your country or countries of citizenship',
        validator=valid_countries,
        widget=widget.Select2Widget(
            values=country_codes,
            multiple=True,
            ),
        oid='citizenships',
    )

    #   birthCountry
    birthCountry = colander.SchemaNode(
        colander.String(),
        title='Country of birth',
        description='Please enter/select your country of birth',
        validator=valid_country,
        widget=widget.Select2Widget(
            values=country_codes),
        oid='birthCountry',
    )

    isnreluser = colander.SchemaNode(
        colander.String(),
        title='Existing NREL Account?',
        description="Select the option that is most true for you.",
        widget=deform.widget.RadioChoiceWidget(values=has_account),
        missing=unicode(''),
        label='Existing or Previous ESIF HPC UserID',
        oid='isnreluser'
    )

    nrelUserID = colander.SchemaNode(
        colander.String(),
        title='Your Existing NREL HPC UserID',
        description='If you have --or previously had-- an NREL UserID, '
                    'enter it here.',
        validator=colander.Length(min=1, max=16),
        widget=widget.TextInputWidget(placeholder='example: jsmythe'),
        missing=unicode(''),
        oid='nrelUserID'
    )

    justification = colander.SchemaNode(
        colander.String(),
        title='NREL HPC User Credential Information',
        widget=widget.TextAreaWidget(rows=6, columns=60),
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
        widget=widget.TextInputWidget(placeholder="example: jsmythe"),
        missing=unicode(''),
        oid='preferredUID'
    )

    comments = colander.SchemaNode(
        colander.String(),
        title='Additional Notes or Comments',
        widget=deform.widget.TextAreaWidget(rows=6, columns=60,
            placeholder='If you think we need any additional '
                'information to process or approve your request, '
                'please let us know.'),
        missing=unicode(''),
        validator=colander.Length(max=1000),
        description='If you think we need any additional '
                'information to process or approve your request, '
                'please let us know.',
        oid='comments'
    )

    #   subTimestamp
    #   couTimestamp
    #   storTimestamp
    #   cyberTimestamp
