import os
import datetime
import string

# from pyramid.response import Response
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config
from pyramid.renderers import get_renderer
# from sqlalchemy.exc import DBAPIError
#import deform
from deform import (ZPTRendererFactory,
                    Form,
                    widget,
                    ValidationFailure)
    # decorator, default_renderer, field, form,
import colander
from pkg_resources import resource_filename

resource_registry = widget.ResourceRegistry()
deform_templates = resource_filename('deform', 'templates')
tpath = os.getcwd()
search_path = (tpath + '/nportal/templates', deform_templates)

drenderer = ZPTRendererFactory(search_path)
# Form.set_zpt_renderer(search_path)
# import htmllaundry
# from htmllaundry import sanitize

from nportal.models import (
    DBSession,
    UserAccountModel
    )

from schemas import AddAccountSchema

from .lists import (us_states,
                    country_codes,
                    title_prefixes,
                    cou_policy,
                    stor_policy,
                    cyber_policy)


def site_layout():
    renderer = get_renderer("../templates/_layout.pt")
    layout = renderer.implementation().macros['layout']
    return layout


class AccountRequestView(object):
    """
    """
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("../templates/_layout.pt")
        #self.layout = renderer.implementation().macros['layout']
        self.layout = site_layout()
        self.title = "Account Request Form"

    @reify
    def account_req_form(self):
        schema = AddAccountSchema().bind(
            country_codes_data=country_codes,
            us_states_data=us_states
        )
        return Form(schema, buttons=('submit',))

    @reify
    def reqts(self, request):
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
            title_prefix_data=title_prefixes,
        )
        Form.set_zpt_renderer(search_path)
        form = Form(schema,
                    action=self.request.route_url('request_user_account'),
                    id='ESIF Account Registration'
                    )

        if 'submit' in self.request.POST:
            # it's a submission, process it
            import pdb; pdb.set_trace()
            controls = self.request.POST.items()




        # not submitted, render form
        return dict(form=form)


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

