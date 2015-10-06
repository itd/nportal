import os
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
from deform import ZPTRendererFactory
from deform import Form
from deform import (widget)  # decorator, default_renderer, field, form,
import colander
from pkg_resources import resource_filename

resource_registry = deform.widget.ResourceRegistry()
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
            return self.add_new_user_account()

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
            title_prefix_data=title_prefixes,
        )
        Form.set_zpt_renderer(search_path)
        form = Form(schema,
                    renderer=drenderer,
                    action=self.request.route_url('request_user_account')
                    )

        #import pdb; pdb.set_trace()
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

