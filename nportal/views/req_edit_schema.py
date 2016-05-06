import deform
import deform.widget
from deform import (widget)  # decorator, default_renderer, field, form,
import colander
from pyramid.renderers import get_renderer

# import htmllaundry
# from htmllaundry import sanitize

from validators import (cyber_validator,
                        phone_validator,
                        stor_validator,
                        cou_validator,
                        valid_country,
                        valid_countries)

from .lists import (approval_status,
                    citizen_types,
                    country_codes,
                    country_codes,
                    employer_types,
                    has_account,
                    has_account,
                    title_prefixes,
                    us_states
                    )


def site_layout():
    renderer = get_renderer("../templates/_layout.pt")
    layout = renderer.implementation().macros['layout']
    return layout


def add_base_template(event):
    base = get_renderer('templates/_layout.pt').implementation()
    event.update({'base': base})


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
    return widget.RadioChoiceWidget(values=approval_status)


@colander.deferred
def deferred_review_status_validator(node, kw):
    return colander.OneOf([x[0] for x in approval_status])


@colander.deferred
def deferred_citizenships_widget(node, kw):
    countries = kw.get('countries', [])
    return widget.SelectWidget(values=countries,
                               multiple=True,
                               )


@colander.deferred
def deferred_citizenships_validator(node, kw):
    countries = kw.get('countries', [])
    return colander.OneOf([x[0] for x in countries])
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


@colander.deferred
def deferred_citizenships_widget(node, kw):
    countries = kw.get('countries', [])
    citz = kw.get('citz', [])
    return widget.SelectWidget(values=citz, multiple=True)


@colander.deferred
def deferred_citizenships_validator(node, kw):
    countries = kw.get('countries', [])
    return colander.OneOf([x[0] for x in countries])


@colander.deferred
def deferred_citz_default(node, kw):
    return kw.get('citz_vals')


@colander.deferred
def deferred_birthcountry_widget(node, kw):
    countries = kw.get('country_codes', [])
    return widget.SelectWidget(values=countries)


# sn_widget = widget.TextInputWidget(css_class='form-control')


class EditRequestSchema(colander.Schema):
    #   cybeTimestamp
    couTimestamp = colander.SchemaNode(
        colander.DateTime(),
        title='Security and Acceptable Use Policy Acceptance',
        description='date',
        widget=widget.DateInputWidget(),
        oid='couTimestamp'
    )

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
        widget=widget.TextInputWidget(),
        oid='sn'
    )

    suffix = colander.SchemaNode(
        colander.String(),
        title='Suffix',
        description='(Sr. Jr. IV, etc.)',
        validator=colander.Length(min=0, max=32),
        widget=widget.TextInputWidget(),
        missing=unicode(''),
        oid='suffix'
    )

    cn = colander.SchemaNode(
        colander.String(),
        title='Common or Nick Name',
        description='Your full name. How you want to be addressed.',
        validator=colander.Length(min=3, max=64),
        widget=widget.TextInputWidget(),
        missing=unicode(''),
        oid='cn'
    )

    street = colander.SchemaNode(
        colander.String(),
        title='Street Address',
        description='',
        validator=colander.Length(min=0, max=200),
        widget=widget.TextInputWidget(),
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
        widget=widget.TextInputWidget(values=country_codes),
        validator=valid_country,
        oid='country'
    )

    mail = colander.SchemaNode(
        colander.String(),
        title='EMail',
        description='Your primary email account',
        widget=widget.TextInputWidget(),
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
        widget=widget.TextInputWidget(),
        oid='phone'
    )

    cell = colander.SchemaNode(
        colander.String(),
        title='Cell phone number',
        description='For contact and verification',
        validator=phone_validator,
        missing=unicode(''),
        widget=widget.TextInputWidget(),
        oid='cell'
    )

    employerType = colander.SchemaNode(
        colander.String(),
        # validator=colander.OneOf([x[0] for x in employer_types]),
        validator=colander.OneOf([x[0] for x in employer_types]),
        widget=deform.widget.RadioChoiceWidget(values=employer_types),
        title='Employer Type',
        description='',
        oid="employerType"
    )

    employerName = colander.SchemaNode(
        colander.String(),
        title='Employer/Institution/Sponsor',
        description='Provided employer or institution name',
        validator=colander.Length(min=3, max=128),
        widget=widget.TextInputWidget(),
        oid='employerName'
    )

    citizenStatus = colander.SchemaNode(
        colander.String(),
        title='Citizenship Status',
        description='Select one of the following options '
                    'that best describes your U.S. citizenship status',
        validator=colander.OneOf([x[0] for x in citizen_types]),
        widget=widget.RadioChoiceWidget(values=citizen_types),
        oid='citizenStatus'
    )

    citizenships = colander.SchemaNode(
        colander.Set(),
        title='Citizenships',
        description='Please select your country or countries of citizenship',
        # validator=valid_countries,
        default=deferred_citz_default,
        widget=deferred_citizenships_widget,
        oid='citizenships',
    )

    birthCountry = colander.SchemaNode(
        colander.String(),
        title='Country of birth',
        description='Please enter/select your country of birth',
        validator=valid_country,
        # widget=widget.Select2Widget(values=country_codes),
        widget=widget.TextInputWidget(),
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
        widget=widget.TextAreaWidget(),
        missing=unicode(''),
        validator=colander.Length(max=1000),
        description="The provided justification/comments for new account.",
        oid='comments'
    )

    preferredUID = colander.SchemaNode(
        colander.String(),
        title='Requested UserID',
        description="The userid the user would prefer",
        validator=colander.Length(min=3, max=16),
        widget=widget.TextInputWidget(),
        missing=unicode(''),
        oid='preferredUID'
    )

    comments = colander.SchemaNode(
        colander.String(),
        title='Additional Notes or Comments',
        widget=widget.TextAreaWidget(),
        missing=unicode(''),
        validator=colander.Length(max=1000),
        description='Additional information',
        oid='comments'
    )

    UserID = colander.SchemaNode(
        colander.String(),
        title='Assigned Permanent HPC UserID',
        description='Determined by Center Operations.'
                    ' This MUST match what is in IDM.',
        validator=colander.Length(min=1, max=16),
        widget=widget.TextInputWidget(),
        default=None,
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
