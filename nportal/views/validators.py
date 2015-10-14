import string
import colander
import htmllaundry

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


def cyber_validator(node, value):
    import pdb; pdb.set_trace()
    if not value:
        raise colander.Invalid(node,
            'You must agree to the Cyber Policies')


def cou_validator(node, value):
    if not value:
        raise colander.Invalid(node,
            'You must agree to the Conditions of Use Policies')


def stor_validator(node, value):
    if not value:
        raise colander.Invalid(node,
            'You must agree to the HPC Storage Policies')
