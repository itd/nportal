import os
from datetime import datetime
from hashids import Hashids
import transaction
import logging
from sqlalchemy.orm import lazyload
from sqlalchemy.orm import joinedload
# from sqlalchemy.orm import (scoped_session, sessionmaker)
from zope.sqlalchemy import ZopeTransactionExtension
import colander
from pyramid.session import SignedCookieSessionFactory
from pyramid.config import (Configurator, settings)
from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.httpexceptions import (
    HTTPMovedPermanently,
    HTTPFound,
    HTTPNotFound,
    )
from deform import (ZPTRendererFactory,
                    Form,
                    widget,
                    ValidationFailure)
    # decorator, default_renderer, field, form,
# import colander
from pkg_resources import resource_filename

from nportal.models import (
    DBSession,
    AccountRequests
    )

from schema_edit_request import EditRequestSchema
from validators import uid_validator
from .lists import (title_prefixes,
                    citizen_types,
                    employer_types,
                    country_codes,
                    has_account,
                    approval_status
                    )


log = logging.getLogger(__name__)

# sqlalchemy setup
# DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),
#                                         expire_on_commit=False))
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


def edit_layout():
    renderer = get_renderer("../templates/_layout_admin.pt")
    layout = renderer.implementation().macros['layout']
    return layout


# def add_base_template(event):
#     base = get_renderer('templates/_layout.pt').implementation()
#     event.update({'base': base})

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


class EditRequestsView(object):
    """
    """
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("../templates/_layout.pt")
        self.layout = edit_layout()
        self.title = "Request Review Form"

        # self.request.session.flash('')
        self.session = request.session

        # see if the POST was a submission
        self.submitted = 'submit' in request.POST
        self.unid = self.request.matchdict['unid']

    @view_config(route_name='req_edit',
                 renderer='../templates/req_edit.pt')
    def edit_request(self):

        """
        /radmin/request/{unid}
        """
        dbsession = DBSession()
        unid = self.request.matchdict['unid']
        data = dbsession.query(AccountRequests).filter_by(unid=unid).one()
        all_countries = country_codes
        # TODO: do a check for came_from also
        success = False
        if data is None:
            title = "Review Request"
            flash_msg = "There was an error processing the request"
            self.request.session.flash(flash_msg)
            rurl = self.request.route_url
            action_url = rurl('req_list')
            return dict(title=title, success=False)

        if self.submitted:
            log.debug('processing submission')
            request = self.request
            controls = request.POST.items()
            captured = None
            log.debug('processing: %s', unid)

            schema = EditRequestSchema().bind(
                countries=[(i[0], i[1]) for i in all_countries],
            )
            dbsession = DBSession()
            data = dbsession.query(AccountRequests).options(
                joinedload('citizenships')).filter_by(unid=unid).one()
            appstruct = data.__dict__

            import pdb; pdb.set_trace()
            # del appstruct['_sa_instance_state']

            appstruct['citizenships'] = ','.join([cc.code for cc
                                                  in data.citizenships])


            form = Form(schema,
                        data=appstruct,
                        action=request.route_url('req_edit', unid=unid),
                        form_id='req_edit')

            try:
                # try to validate the submitted values
                captured = form.validate(controls)

            except ValidationFailure as e:
                # the submitted values could not be validated
                flash_msg = u"Please address the errors indicated below!"
                request.session.flash(flash_msg)
                return dict(form=form, data=appstruct, page_title=self.title)

            unid = _update_request(appstruct, data, request)
            view_url = request.route_url('req_edit',
                                         unid=unid,
                                         page_title="Request Updated")

            return HTTPFound(view_url,
                             action=request.route_url('req_edit', unid=unid),
                             data=appstruct)
            # return HTTPMovedPermanently(location=view_url)
            # return self.request_received_view()
            # return view_url


        rev_status = [i[0] for i in approval_status]
        schema = EditRequestSchema().bind(   ## validator=uid_validator
            cou=data.couTimestamp.strftime('%Y-%m-%d %H:%M')
        )

        title = "Review Request"
        # flash_msg = None
        # self.request.session.flash(flash_msg)

        rurl = self.request.route_url
        action_url = rurl('req_edit', unid=unid)

        appstruct = data.__dict__

        as_citizenships = appstruct['citizenships']
        clist = [dbsession.query(AccountRequests).filter_by(unid=i).first()
                     for i in as_citizenships]
        appstruct['citizenships'] = clist
        # appstruct['couTimestamp'] = data.couTimestamp
        appstruct['citizenships'] = ','.join([cc.code for cc
                                              in data.citizenships])

        form = Form(schema,
                    buttons=('submit',),
                    action=action_url,
                    appstruct=appstruct)

        return dict(title=title,
                    action=action_url,
                    form=form,
                    data=appstruct,
                    success=True)


def _update_request(appstruct, data, request):
    ai = appstruct.items()
    ai = dict(ai)
    dbsess = DBSession()

    # now = now.strftime('%y%m%d%H%M%S')
    now = datetime.now()
    unid = ai['unid']
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
    # mailPreferred = ai['mailPreferred']
    phone = ai['phone']
    cell = ai['cell']
    employerType = ai['employerType']
    employerName = ai['employerName']
    citizenStatus = ai['citizenStatus']
    # citizenships = [dbsess.query(CountryCodes
    #                 ).filter(CountryCodes.code == i).one()
    #                 for i in ai['citizenships']]
    birthCountry = ai['birthCountry']
    nrelUserID = ai['nrelUserID']
    preferredUID = ai['preferredUID']
    justification = ai['justification']
    comments = ai['comments']
    couTimestamp  = ai['couTimestamp']
    storTimestamp = ai['storTimestamp']
    subTimestamp  = ai['subTimestamp']
    approvalStatus = ai['approvalStatus']
    UserID = ai['UserID']

    if not cn:
        cn = "%s, %s" % (givenName, sn)

    submission = AccountRequests(
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
        # mailPreferred=mailPreferred,
        phone=phone,
        cell=cell,
        employerType=employerType,
        employerName=employerName,
        citizenStatus=citizenStatus,
        # citizenships=citizenships,
        birthCountry=birthCountry,
        nrelUserID=nrelUserID,
        preferredUID=preferredUID,
        justification=justification,
        comments=comments,
        approvalStatus=approvalStatus,
        UserID=UserID,
        subTimestamp=subTimestamp,
        couTimestamp=couTimestamp,
        storTimestamp=storTimestamp,
        )

    # write the data
    dbsess.add(submission)
    transaction.commit()
    # return the unid for processing in next form
    return str(unid)
