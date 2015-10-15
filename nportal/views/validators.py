import string
import colander
import htmllaundry
from .lists import country_codes


def phone_validator(node, value):
    """ checks to make sure that the value looks like a phone number """
    value = htmllaundry.strip_markup(value)
    allowed = set(string.ascii_lowercase + string.digits + ' ' + '.' + '+' + '(' + ')' + '-')
    tval = set(value) <= allowed

    if value is u'':
        raise colander.Invalid(node,
               'Please provide a valid phone number')
    if not tval:
        raise colander.Invalid(node,
               '%s is not a valid telephone number format' % value)


def cou_validator(node, value):
    if not value:
        raise colander.Invalid(node,
            'You must agree to the Conditions of Use Policies')


def stor_validator(node, value):
    if not value:
        raise colander.Invalid(node,
            'You must agree to the HPC Storage Policies')


def cyber_validator(node, value):
    if not value:
        raise colander.Invalid(node,
            'You must agree to the Cyber Policies')


def valid_country(node, value):
    cs = [x[0] for x in country_codes]
    if value not in cs:
        msg = u'You must select a valid country'
        raise colander.Invalid(node, msg)


def valid_countries(node, value):
    cs = set([x[0] for x in country_codes])
    if not value.intersection(cs):
        print('not there')
        msg = u'You must select one or more countries'
        raise colander.Invalid(node, msg)
