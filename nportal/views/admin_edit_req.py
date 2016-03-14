import os
from datetime import datetime
import string
from hashids import Hashids
import requests
import transaction

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import (scoped_session, sessionmaker)

from pyramid.security import authenticated_userid
# from pyramid.response import Response
from pyramid.decorator import reify
from pyramid.httpexceptions import (
    HTTPMovedPermanently,
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.session import SignedCookieSessionFactory

from pyramid.config import (Configurator, settings)

from pyramid.view import view_config
from pyramid.renderers import get_renderer, render, render_to_response
# from sqlalchemy.exc import DBAPIError
#import deform
from deform import (ZPTRendererFactory,
                    Form,
                    widget,
                    ValidationFailure)
    # decorator, default_renderer, field, form,
import colander
from pkg_resources import resource_filename

from nportal.models import (
    DBSession,
    UserRequest,
    CountryCodes,
    #Citizenship
    )

from schema_edit_acount import EditAccountSchema
from validators import uid_validator
from .lists import (us_states,
                    country_codes,
                    title_prefixes,
                    has_account,
                    )

from .schemas import AddAccountSchema

# sqlalchemy setup
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),
                                        expire_on_commit=False))
sess = DBSession()

# view flash session info
req_session_factory = SignedCookieSessionFactory('itsaseekreet')
config = Configurator()
config.set_session_factory(req_session_factory)

# deform retail form additions
resource_registry = widget.ResourceRegistry()
deform_templates = resource_filename('deform', 'templates')
tpath = os.getcwd()
search_path = (tpath + '/nportal/templates', deform_templates)
drenderer = ZPTRendererFactory(search_path)
# Form.set_zpt_renderer(search_path)
# import htmllaundry
# from htmllaundry import sanitize


def edit_layout():
    renderer = get_renderer("../templates/_layout_admin.pt")
    layout = renderer.implementation().macros['layout']
    return layout


# def add_base_template(event):
#     base = get_renderer('templates/_layout.pt').implementation()
#     event.update({'base': base})


class EditRequestsView(object):
    """
    """
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("../templates/_layout_admin.pt")
        self.layout = edit_layout()
        self.title = "Request Update Form"

    @view_config(route_name='req_edit',
                 renderer='../templates/req_edit.pt')
    def edit_request(self):

        """
        /radmin/request/{unid}
        """
        unid = self.request.matchdict['unid']
        session = DBSession()
        u_data = session.query(UserRequest).filter_by(unid=unid).one()
        # TODO: do a check for came_from also

        # Do a check to ensure user data is there...
        success = False
        if u_data is None:
            title = "Request Update"
            flash_msg = "There was an error processing the submission"
            self.request.session.flash(flash_msg)
            return dict(title=title, success=False)

        schema = AddAccountSchema()

        rurl = self.request.route_url
        action_url = rurl('req_list')
        reg_form = Form(schema,
                        buttons=('submit', 'delete'),
                        action=action_url,
                        logged_in=authenticated_userid(self.request)
                        )

        title = "Edit Request"
        flash_msg = "Success! Your request has been submitted."
        self.request.session.flash(flash_msg)

        form = Form(schema, buttons=('submit',))

        appstruct = u_data.__dict__
        del appstruct['_sa_instance_state']
        import pdb; pdb.set_trace()

        return dict(title=title,
                    form=form.render(appstruct=appstruct),
                    data=u_data,
                    success=True)

        # # self.request.session.flash('')
        # request = self.request
        # session = request.session
        # Form.set_zpt_renderer(search_path)
        #
        # # see if a user submitted the form
        # submitted = 'submit' in request.POST
        #
        # # get the user email from the POST request, if present
        # user_email = request.POST.get('email', '')
        #
        # # get the form control field names and values as a list of tuples
        # controls = request.POST.items()
        #
        # # create a deform form object from the schema
        # form = Form(schema,
        #             action=request.route_url('request_user_account'),
        #             form_id='deformRegform'
        #             )
        #
        # if submitted:
        #     # it's a submission, process it
        #     controls = self.request.POST.items()
        #     captured = None
        #
        #     # schema = schema(validator=uid_validator)
        #     # create a deform form object from the schema
        #     sform = Form(schema,
        #                  action=request.route_url('request_user_account'),
        #                  form_id='deformRegform')
        #
        #     try:
        #         # try to validate the submitted values
        #         captured = sform.validate(controls)
        #
        #     except ValidationFailure as e:
        #         # the submitted values could not be validated
        #         flash_msg = u"Please address the errors indicated below!"
        #         self.request.session.flash(flash_msg)
        #         return dict(form=sform, page_title=self.title)
        #
        #
        #     # The checks passed.
        #     # request.session.flash("It submitted! (not really)")
        #     # submit the data to be added to be recorded,
        #     # return a unique identifier - unid
        #     unid = _update_request(captured, request)
        #     title = 'Update Successfully submitted '
        #     view_url = request.route_url('request_received_view',
        #                                  unid=unid, page_title=title)
        #     return HTTPFound(view_url)
        #     # return HTTPMovedPermanently(location=view_url)
        #     # return self.request_received_view()
        #     # return view_url
        #
        # else:
        #     # not submitted, render form
        #     return dict(form=form, page_title=self.title)


    # http://goo.gl/KnNbAK
    # https://pypi.python.org/pypi/hashids/
    #
    # @view_config(route_name='req_editx',
    #              renderer='../templates/req_edit.pt')
    # def request_received_view(self):
    #     unid = self.request.matchdict['unid']
    #     session = DBSession()
    #     u_data = session.query(UserRequest).filter_by(unid=unid).first()
    #     # TODO: do a check for came_from also
    #
    #     # Do a check to ensure user data is there...
    #     success = False
    #     if u_data is None:
    #         title = "Account Request Submission Error"
    #         flash_msg = "There was an error processing the request"
    #         self.request.session.flash(flash_msg)
    #         return dict(title=title, success=False)
    #
    #     title = "Account Request Successfully Submitted"
    #     flash_msg = "Success! Your request has been submitted."
    #     self.request.session.flash(flash_msg)
    #     return dict(title=title,
    #                 data=u_data,
    #                 success=True)


def _update_request(appstruct, request):
    regset = request.registry.settings
    slt = regset['unid_salt']
    hashids = Hashids(salt=slt)
    unid = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    ai = appstruct.items()
    ai = dict(ai)
    dbsess = DBSession()

    # now = now.strftime('%y%m%d%H%M%S')
    now = datetime.now()
    unid = hashids.encode(int(unid))
    givenName = ai['givenName']
    middleName = ai['middleName']
    sn = ai['sn']
    suffix = ai['suffix']
    cn = ai['cn']
    street = ai['street']
    lcity = ai['lcity']
    st = ai['st']
    postalCode = ai['postalCode']
    country = ai['country']
    mail = ai['mail']
    mailPreferred = ai['mailPreferred']
    phone = ai['phone']
    cell = ai['cell']
    employerType = ai['employerType']
    employerName = ai['employerName']
    citizenStatus = ai['citizenStatus']
    citizenships = [dbsess.query(CountryCodes
                    ).filter(CountryCodes.code == i).one()
                    for i in ai['citizenships']]
    birthCountry = ai['birthCountry']
    nrelUserID = ai['nrelUserID']
    preferredUID = ai['preferredUID']
    justification = ai['justification']
    comments = ai['comments']
    couTimestamp = now
    storTimestamp = now
    subTimestamp = now

    if not cn:
        cn = "%s, %s" % (givenName, sn)

    submission = UserRequest(
        unid=unid,
        givenName=givenName,
        middleName=middleName,
        sn=sn,
        suffix=suffix,
        cn=cn,
        street=street,
        lcity=lcity,
        st=st,
        postalCode=postalCode,
        country=country,
        mail=mail,
        mailPreferred=mailPreferred,
        phone=phone,
        cell=cell,
        employerType=employerType,
        employerName=employerName,
        citizenStatus=citizenStatus,
        citizenships=citizenships,
        birthCountry=birthCountry,
        nrelUserID=nrelUserID,
        preferredUID=preferredUID,
        justification=justification,
        comments=comments,
        subTimestamp=subTimestamp,
        couTimestamp=couTimestamp,
        storTimestamp=storTimestamp
        )

    # write the data
    dbsess.add(submission)
    transaction.commit()
    # return the unid for processing in next form
    return str(unid)
