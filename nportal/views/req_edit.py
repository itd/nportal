import os
from datetime import datetime
import transaction
import logging
import colander
from sqlalchemy.orm import lazyload
from sqlalchemy.orm import joinedload
# from sqlalchemy.orm import (scoped_session, sessionmaker)
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.session import SignedCookieSessionFactory
from pyramid.config import (Configurator, settings)
from pyramid.view import view_config
from pyramid.renderers import get_renderer
from pyramid.httpexceptions import (HTTPFound, HTTPNotFound)
from pyramid.security import authenticated_userid
import deform
from deform import (Form,
                    widget,
                    Button,
                    ValidationFailure)

from nportal.models import (
    DBSession,
    AccountRequests,
    Citizenships
    )

from req_edit_schema import EditRequestSchema
from validators import uid_validator
from .lists import (title_prefixes,
                    citizen_types,
                    employer_types,
                    country_codes,
                    has_account,
                    approval_status
                    )


log = logging.getLogger(__name__)

# # view flash session info
# req_session_factory = SignedCookieSessionFactory('itsaseekreet')
# config = Configurator()
# config.set_session_factory(req_session_factory)

# # deform retail form additions
# resource_registry = widget.ResourceRegistry()
# deform_templates = resource_filename('deform', 'templates')
# tpath = os.getcwd()
# search_path = (tpath + '/nportal/templates', deform_templates)
# drenderer = ZPTRendererFactory(search_path)


def edit_layout():
    renderer = get_renderer("../templates/_layout_admin.pt")
    layout = renderer.implementation().macros['layout']
    return layout


# def add_base_template(event):
#     base = get_renderer('templates/_layout.pt').implementation()
#     event.update({'base': base})

# @colander.deferred
# def deferred_country_widget(node, kw):
#     country_codes_data = kw.get('country_codes_data', [])
#     return widget.Select2Widget(values=country_codes_data)
#
#
# @colander.deferred
# def deferred_state_widget(node, kw):
#     us_states_data = kw.get('us_states_data', [])
#     return widget.Select2Widget(values=us_states_data)
#
#
# @colander.deferred
# def deferred_title_prefix_widget(node, kw):
#     title_prefix_data = kw.get('title_prefix_data', [])
#     return widget.Select2Widget(values=title_prefix_data)

def merge_dbsession_with_post(session, post):
    for key, value in post:
        setattr(session, key, value)
    return session


def merge_appstruct(adbsession, appstruct):
    for key in appstruct.keys():
        setattr(adbsession, key, appstruct[key])
    return adbsession

def record_to_appstruct(ob):
    return dict([(k, ob.__dict__[k])
                 for k in sorted(ob.__dict__)
                 if '_sa_' != k[:4]])


class EditRequestsView(object):
    """
    """
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("../templates/_layout_admin.pt")
        self.layout = renderer.implementation().macros['layout']
        self.session = request.session
        self.dbsession = DBSession()

    # @property
    # def req_edit_form(self):
    #     schema = EditRequestSchema()
    #     return deform.Form(schema, buttons=('submit',))
    #
    # @property
    # def reqts(self):
    #     return self.req_edit_form.get_widget_resources()

    @view_config(route_name='req_edit',
                 renderer='../templates/req_edit_retail.pt')
    def edit_request(self):

        """
        /radmin/request/{unid}
        """
        unid = self.request.matchdict['unid']
        obj = DBSession.query(AccountRequests
                              ).options(joinedload('citizenships')
                                        ).filter_by(unid=unid).one()
        request = self.request
        sess = self.dbsession
        title = "Request Review - %s" % unid
        if obj is None:
            return HTTPNotFound('No Account Request exists with that ID.')

        title = "Edit Req "
        schema = EditRequestSchema().bind(
            cou=obj.couTimestamp.strftime('%Y-%m-%d %H:%M'),
            countries=country_codes,
            request=request,
        )
        action_url = self.request.route_url('req_edit',
                          #logged_in=authenticated_userid(self.request),
                          unid=unid)

        submit = deform.Button(name='submit', css_class='red')
        # return deform.Form(schema, buttons=(submit,))
        form = Form(schema)

        if 'submit' in request.params:
            log.debug('processing submission')
            controls = request.POST.items()
            log.debug('processing edit: %s', request.matchdict['unid'])

            try:
                # try to validate the submitted values
                appstruct = form.validate(controls)

            except deform.ValidationFailure, e:
                # the submitted values could not be validated
                flash_msg = u"Please address the errors indicated below!"
                request.session.flash(flash_msg)

                return dict(form=form,
                            data=obj,
                            page_title=title,
                            action=request.route_url('req_edit', unid=unid))

            # citizenships = appstruct['citizenships']
            # clist = [sess.query().filter_by(citizenships=i).first()
            #          for i in citizenships]
            # appstruct['citizenships'] = clist
            #
            # record = merge_dbsession_with_post(obj, appstruct)

            # all good
            appstruct['citizenships'] = obj.citizenships
            appstruct['couTimestamp'] = obj.couTimestamp
            appstruct['subTimestamp'] = obj.subTimestamp
            appstruct['storTimestamp'] = obj.storTimestamp
            _update_request(appstruct, obj)

            flash_msg = u"Request Updated"
            request.session.flash(flash_msg)
            view_url = request.route_url(
                'req_edit',
                unid=unid,
                page_title="Request Updated",
                # logged_in=authenticated_userid(self.request)
            )
            action = request.route_url('req_edit', unid=unid)

            return HTTPFound(view_url)

        # not a submission, view
        unid = request.matchdict['unid']
        dbsession = DBSession()
        data = dbsession.query(AccountRequests
                               ).options(joinedload('citizenships')
                                         ).filter_by(unid=unid).one()
        aps = data.__dict__
        # approvalStatusValues
        # aps['approvalStatusValues'] = approval_status

        schema = EditRequestSchema().bind(
            countries=country_codes,
            request=request,
            citz=[(i.code, i.name) for i in aps['citizenships']],
            citz_vals=[i.code for i in aps['citizenships']]
        )

        acs = aps['citizenships']
        #cit_list = [dict([('code', i.code), ('name', i.name)]) for i in acs]
        cit_list = [(i.code, i.name) for i in acs]

        aps['citizenships'] = cit_list
        # submit = deform.Button(name='submit', css_class='red')
        # # return deform.Form(schema, buttons=(submit,))
        # form = Form(schema,
        #             buttons=(submit,),
        #             action=action_url)

        appstruct = record_to_appstruct(data)
        cancel = Button(name='cancel', css_class='foo', value='cancelled')
        submit = Button(name='submit', css_class='red')

        form = Form(schema,
                    appstruct=aps,
                    buttons=(submit,),
                    action=action_url)

        return dict(title=title,
                    action=action_url,
                    form=form,
                    data=aps,
                    success=True)


def _update_request(appstruct, obj):
    ai = appstruct
    # ai = dict(ai)
    dbsess = DBSession()
    unid = obj.unid
    rec = DBSession.query(AccountRequests
                      ).options(joinedload('citizenships')
                                ).filter_by(unid=unid).one()
    # now = now.strftime('%y%m%d%H%M%S')
    now = datetime.now()

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
    citizenships = ai['citizenships']
    #[dbsess.query(Citizenships).filter(Citizenships.code == i).one() for i in ai['citizenships']]
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

    rec.unid = unid
    rec.givenName = givenName
    rec.middleName = middleName
    rec.sn = sn
    rec.suffix = suffix
    rec.cn = cn
    rec.street = street
    rec.lcity = lcity
    rec.st = st
    rec.postalCode = postalCode
    rec.country = country
    rec.mail = mail
    # mailPreferred = mailPreferred
    rec.phone = phone
    rec.cell = cell
    rec.employerType = employerType
    rec.employerName = employerName
    rec.citizenStatus = citizenStatus
    # obj.citizenships = citizenships
    rec.birthCountry = birthCountry
    rec.nrelUserID = nrelUserID
    rec.preferredUID = preferredUID
    rec.justification = justification
    rec.comments = comments
    rec.approvalStatus = approvalStatus
    rec.UserID = UserID
    rec.subTimestamp = subTimestamp
    rec.couTimestamp = couTimestamp
    rec.storTimestamp = storTimestamp

    # write the data
    transaction.commit()
    # return the unid for processing in next form
    return str(unid)
