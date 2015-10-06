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
                    citizen_types)


@colander.deferred
def deferred_country_widget(node, kw):
    country_codes_data = kw.get('country_codes_data', [])
    return widget.SelectWidget(values=country_codes_data)

@colander.deferred
def deferred_state_widget(node, kw):
    us_states_data = kw.get('us_states_data', [])
    return widget.SelectWidget(values=us_states_data)

@colander.deferred
def deferred_title_prefix_widget(node, kw):
    title_prefix_data = kw.get('title_prefix_data', [])
    return widget.SelectWidget(values=title_prefix_data)

email_confirm_widget = deform.widget.CheckedInputWidget(
            subject='Email',
            confirm_subject='Confirm Email',
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
        title='Title/Prefix:',
        description='If you prefer to use a title, enter it here.',
        validator=colander.ContainsOnly([x[0] for x in title_prefixes]),
        widget=deferred_title_prefix_widget,
        oid='titlePrefix'
    )

    givenName = colander.SchemaNode(
        colander.String(),
        title='First Name/Given Name',
        description='Your legal First Name.',
        validator=colander.Length(min=1, max=64),
        widget=widget.TextInputWidget(placeholder='Your legal First Name.'),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='givenName'
    )

    sn = colander.SchemaNode(
        colander.String(),
        title='Last Name',
        description='Your legal family name or last name.',
        validator=colander.Length(min=1, max=64),
        widget=widget.TextInputWidget(
            placeholder='Your legal family name or last name.'),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='sn'
    )

    middleName = colander.SchemaNode(
        colander.String(),
        title='Middle Name',
        description='Your legal middle name if applicable.',
        validator=colander.Length(min=0, max=64),
        widget=widget.TextInputWidget(
            placeholder='Your legal middle name if applicable.'),
        missing=unicode(''),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='middleName'
    )

    suffix = colander.SchemaNode(
        colander.String(),
        title='Suffix',
        description='(Sr. Jr. IV, etc.)',
        validator=colander.Length(min=0, max=32),
        widget=widget.TextInputWidget(),
        missing=unicode(''),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='suffix'
    )

    userTitle = colander.SchemaNode(
        colander.String(),
        title='Title',
        description='A title you may currently use',
        validator=colander.Length(min=0, max=128),
        widget=widget.TextInputWidget(),
        missing=unicode(''),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='userTitle'
    )

    cn = colander.SchemaNode(
        colander.String(),
        title='Common or Nick Name',
        description='Your full name. How you want to be addressed.',
        validator=colander.Length(min=2, max=64),
        widget=widget.TextInputWidget(
            placeholder='How you want to be addressed: Pat Marlinski'),
        missing=unicode(''),
        preparer=[strip_whitespace, remove_multiple_spaces],
        oid='cn'
    )

    street = colander.SchemaNode(
        colander.String(),
        title='Street Address',
        description='',
        validator=colander.Length(min=0, max=200),
        widget=widget.TextAreaWidget(placeholder='example: 123 Noe Way'),
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
        widget=widget.TextInputWidget(
            placeholder='Please provide your primary telephone number'),
        oid='phone'
    )

    cell = colander.SchemaNode(
        colander.String(),
        title='Cell',
        description='We will use your cell phone number for verification',
        validator=phone_validator,
        missing=unicode(''),
        preparer=[strip_whitespace, remove_multiple_spaces],
                widget=widget.TextInputWidget(
            placeholder='for verification and contact'),
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
    #
    # shipAddrSame = colander.SchemaNode(
    #     colander.Bool(),
    #     title='Shipping Address',
    #     description='click if this is the same as above',
    #     widget=widget.CheckboxWidget(),
    #     oid='shipAddrSame'
    # )
    #
    # shipAddr = colander.SchemaNode(
    #     colander.String(),
    #     missing=None,
    #     title='Address',
    #     description='Your shipping address - in case we need to send you a physical VPN token.',
    #     validator=colander.Length(min=0, max=128),
    #     widget=widget.TextInputWidget(),
    #     preparer=[strip_whitespace, htmllaundry.sanitize],
    #     oid='shipAddr'
    # )
    #
    #
    # shipAddrCity = colander.SchemaNode(
    #     colander.String(),
    #     title='City',
    #     description='',
    #     validator=colander.Length(min=0, max=128),
    #     widget=widget.TextInputWidget(),
    #     preparer=[strip_whitespace, remove_multiple_spaces,
    #               htmllaundry.sanitize],
    #     oid='shipAddrCity'
    # )
    #
    # shipAddrState = colander.SchemaNode(
    #     colander.String(),
    #     title='State / Province / Region',
    #     description='',
    #     validator=colander.Length(min=0, max=64),
    #     widget=widget.TextInputWidget(),
    #     preparer=[strip_whitespace, remove_multiple_spaces, sanitize],
    #     oid='shipAddrCity'
    # )
    #
    # shipAddrPostCode = colander.SchemaNode(
    #     colander.String(),
    #     title='Postal Code / Zip',
    #     description='',
    #     validator=colander.Length(min=0, max=64),
    #     widget=widget.TextInputWidget(),
    #     preparer=[htmllaundry.sanitize],
    #     oid='shipAddr'
    # )
    #
    # shipAddrCountry = colander.SchemaNode(
    #     colander.String(),
    #     title='',
    #     description='',
    #     validator=colander.Length(min=0, max=64),
    #     widget=deferred_country_widget,
    #     preparer=[strip_whitespace, remove_multiple_spaces],
    #     oid='shipAddrCountry',
    # )
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
