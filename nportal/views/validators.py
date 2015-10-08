import string
import colander

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
