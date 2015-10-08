import deform
import deform.widget
from deform import (widget)  # decorator, default_renderer, field, form,
import colander
import htmllaundry
from htmllaundry import sanitize

from validators import (cyber_validator, phone_validator)

from nportal.views import (strip_whitespace,
                           remove_multiple_spaces,
                           rm_spaces
                           )

from .lists import (title_prefixes,
                    citizen_types,
                    employer_types,
                    country_codes,
                    cou_policy,
                    stor_policy,
                    cyber_policy
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
            subject='Email',
            confirm_subject='Confirm your Email',
            )

sn_widget = widget.TextInputWidget(
            css_class='form-control')

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
        widget=deform.widget.CheckboxChoiceWidget(values=cou_policy),
        oid='cou'
    )

    #   storTimestamp
    stor = colander.SchemaNode(
        colander.Boolean(),
        title='Storage Acceptance',
        description='Check this if you have read and agree '
                    'to the Center\'s storage policies.',
        widget=deform.widget.CheckboxChoiceWidget(values=stor_policy),
        oid='stor'
    )
    #   cybeTimestamp
    cyber = colander.SchemaNode(
        colander.Boolean(),
        title='Cyber Security Policy Acceptance',
        description='Check this if you have read and agree to abide by '
                    'the Center\'s Cyber Security policies.',
        widget=deform.widget.CheckboxChoiceWidget(values=cyber_policy),
        validator=cyber_validator,
        oid='stor'
    )

    titlePrefix = colander.SchemaNode(
        colander.String(),
        title='Hornorary',
        description='If you prefer to use n honorary, enter it here.',
        # validator=colander.ContainsOnly([x[0] for x in title_prefixes]),
        validator=colander.Length(min=1, max=64),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        widget=widget.TextInputWidget(placeholder="Dr., Mr., Ms., etc."),
        missing=unicode(''),
        oid='titlePrefix'
    )

    # userTitle = colander.SchemaNode(
    #     colander.String(),
    #     title='Title',
    #     description='A title you may currently use',
    #     validator=colander.Length(min=0, max=128),
    #     widget=widget.TextInputWidget(placeholder="ex.: Sr. Scientist"),
    #     missing=unicode(''),
    #     preparer=[strip_whitespace, remove_multiple_spaces,
    #               htmllaundry.sanitize],
    #     oid='userTitle'
    # )

    givenName = colander.SchemaNode(
        colander.String(),
        title='Given or first name',
        description='Your given or first name',
        validator=colander.Length(min=1, max=64),
        widget=widget.TextInputWidget(placeholder=''),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        oid='givenName'
    )

    middleName = colander.SchemaNode(
        colander.String(),
        title='Middle name/initial',
        description='Middle name or initial',
        validator=colander.Length(min=0, max=64),
        widget=widget.TextInputWidget(
            placeholder=''),
        missing=unicode(''),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        oid='middleName'
    )

    sn = colander.SchemaNode(
        colander.String(),
        title='Family / Last Name',
        description='family Name / Last Name',
        validator=colander.Length(min=1, max=64),
        widget=widget.TextInputWidget(
            placeholder=''),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        oid='sn'
    )

    suffix = colander.SchemaNode(
        colander.String(),
        title='Suffix',
        description='(Sr. Jr. IV, etc.)',
        validator=colander.Length(min=0, max=32),
        widget=widget.TextInputWidget(placeholder='exaple: RHCE, PhD, etc.'),
        missing=unicode(''),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        oid='suffix'
    )

    cn = colander.SchemaNode(
        colander.String(),
        title='Common or Nick Name',
        description='Your full name. How you want to be addressed.',
        validator=colander.Length(min=2, max=64),
        widget=widget.TextInputWidget(
            placeholder='How you want to be addressed: Pat Marlinski'),
        missing=unicode(''),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        oid='cn'
    )

    street = colander.SchemaNode(
        colander.String(),
        title='Street Address',
        description='',
        validator=colander.Length(min=0, max=200),
        widget=widget.TextInputWidget(placeholder='example: 123 Noe Way'),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        oid='street'
    )

    l = colander.SchemaNode(
        colander.String(),
        title='City',
        description='',
        validator=colander.Length(min=1, max=128),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        oid='l'
    )

    st = colander.SchemaNode(
        colander.String(),
        title='State / Province / Region',
        description='',
        validator=colander.Length(min=1, max=128),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        oid='l'
    )

    postalCode = colander.SchemaNode(
        colander.String(),
        title='Post Code / ZIP Code',
        description='',
        validator=colander.Length(min=0, max=64),
        widget=widget.TextInputWidget(),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        oid='postalCode'
    )

    country = colander.SchemaNode(
        colander.String(),
        title='Country',
        description='',
        widget=widget.SelectWidget(values=country_codes),
        oid='country'
    )

    mail = colander.SchemaNode(
        colander.String(),
        title='EMail',
        description='Your primary email account',
        validator=colander.Email(msg="Please provide a valid Email address"),
        preparer=[rm_spaces, htmllaundry.sanitize,
                  htmllaundry.sanitize],
        widget=email_confirm_widget,
        oid='mail'
    )
    phone = colander.SchemaNode(
        colander.String(),
        title='Phone number',
        description='Please provide your primary telephone number',
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        validator=phone_validator,
        widget=widget.TextInputWidget(
            placeholder='ex: 000-000-0000'),
        oid='phone'
    )

    cell = colander.SchemaNode(
        colander.String(),
        title='Cell phone number',
        description='For contact and verification',
        validator=phone_validator,
        missing=unicode(''),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
                widget=widget.TextInputWidget(
            placeholder='ex +1-000-000-0000'),
        oid='cell'
    )

    employerType = colander.SchemaNode(
        colander.Int(),
        validator=colander.OneOf([x[0] for x in employer_types]),
        widget=deform.widget.RadioChoiceWidget(values=employer_types),
        title='Employer Type',
        description='Select the employer type from the list below that '
        'is most appropriate to your request',
        oid="employerType"
    )

    # employerSponsor = colander.SchemaNode(
    #     colander.Boolean(),
    #     title='Employment/Institution supporting this work',
    #     description='click if the same as employer above',
    #     widget=widget.CheckboxWidget(),
    #     oid='employerSponsor'
    # )
    #
    employerName = colander.SchemaNode(
        colander.String(),
        title='Employer / Sponsor Name',
        description='Please provide the name of the employer or institution you represent',
        validator=colander.Length(min=0, max=128),
        widget=widget.TextInputWidget(placeholder='employer/institution name here'),
        preparer=[strip_whitespace, remove_multiple_spaces,
                  htmllaundry.sanitize],
        oid='employerName'
    )

    citizenStatus = colander.SchemaNode(
        colander.Boolean(),
        title='Citizenship Status',
        description='Select one of the following options '
            'that best describes your U.S. citizenship status',
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
        colander.Set(),
        title='Citizen of',
        description='Please enter your country(s) of citizenship',
        validator=colander.ContainsOnly([x[0] for x in country_codes]),
        widget=widget.Select2Widget(
            values=country_codes,
            multiple=True,
            ),
        oid='citizenOf',
    )

    #   birthCountry

    nrelExistingAccount = colander.SchemaNode(
        colander.Boolean(),
        title='Existing NREL Account?',
        description='If you\'ve used an NREL HPC account, check this.',
        widget=deform.widget.CheckboxWidget(),
        label='I have an Existing or Previous NREL Account',
        oid='nrelExistingAccount'
    )

    nrelUserID = colander.SchemaNode(
        colander.String(),
        title='Existing NREL UserID?',
        description='If you have --or have previously had-- an NREL UserID, '
                    'please enter it here.',
        validator=colander.Length(min=1, max=16),
        widget=widget.TextInputWidget(placeholder='example: jsmythe'),
        missing=unicode(''),
        preparer=[htmllaundry.sanitize, strip_whitespace],
        oid='nrelUserID'
    )

    #   preferredUID
    preferredUID = colander.SchemaNode(
        colander.String(),
        title='UserID',
        description="If you have -or have previously been given- "
                    "an NREL account or UserID, enter that ID. "
                    "If you've never had an NREL account, "
                    "tell us what you'd like to use for a login UserID"
                    "(3 to 16 characters, all lower case.)",
        validator=colander.Length(min=3, max=16),
        widget=widget.TextInputWidget(placeholder="example: jsmythe"),
        missing=unicode(''),
        preparer=[htmllaundry.sanitize, strip_whitespace],
        oid='preferredUID'
    )

    justification = colander.SchemaNode(
        colander.String(),
        title='Account Request Justification',
        widget=deform.widget.TextAreaWidget(rows=6, columns=60),
        preparer=[htmllaundry.sanitize],
        validator=colander.Length(max=1000),
        description='Briefly describe how you plan to use the '
                    'ESIF HPC Resources. Include relevant '
                    'project names and contacts if available.',
        oid='comments'
    )

    comments = colander.SchemaNode(
        colander.String(),
        title='Comments',
        widget=deform.widget.TextAreaWidget(rows=6, columns=60,
            placeholder='If you think we need any additional '
                'information to process or approve your request, '
                'please let us know.'),
        missing=unicode(''),
        preparer=[htmllaundry.sanitize],
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
