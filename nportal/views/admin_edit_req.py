import os
from datetime import datetime
from hashids import Hashids
import transaction

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import (scoped_session, sessionmaker)

from pyramid.session import SignedCookieSessionFactory
from pyramid.config import (Configurator, settings)
from pyramid.view import view_config
from pyramid.renderers import get_renderer
from deform import (ZPTRendererFactory,
                    Form,
                    widget,
                    ValidationFailure)
    # decorator, default_renderer, field, form,
# import colander
from pkg_resources import resource_filename

from nportal.models import (
    DBSession,
    Request,
    CountryCodes,
    user_citizen
    )

from schema_edit_request import EditRequestSchema
from validators import uid_validator
from .lists import (us_states,
                    country_codes,
                    title_prefixes,
                    has_account,
                    )


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


class EditRequestsView(object):
    """
    """
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("../templates/_layout.pt")
        self.layout = edit_layout()
        self.title = "Request Review Form"

    @view_config(route_name='req_edit',
                 renderer='../templates/req_edit.pt')
    def edit_request(self):

        """
        /radmin/request/{unid}
        """
        unid = self.request.matchdict['unid']
        session = DBSession()
        data = session.query(Request).filter_by(unid=unid).one()
        # TODO: do a check for came_from also

        # Do a check to ensure user data is there...
        success = False
        if data is None:
            title = "Review Request"
            flash_msg = "There was an error processing the submission"
            self.request.session.flash(flash_msg)
            rurl = self.request.route_url
            action_url = rurl('req_list')
            return dict(title=title, success=False)

        # cz = session.query(Request).filter(
        #          Request.citizenships.any(unid=u_data.unid))
        # cz = session.query(Request).filter(unid=u_data.unid)

        schema = EditRequestSchema().bind(   ## validator=uid_validator
            cou=data.couTimestamp.strftime('%Y-%m-%d %H:%M'),
        )
        title = "Review Request"
        flash_msg = "Success! The request has been updated."
        self.request.session.flash(flash_msg)

        rurl = self.request.route_url
        action_url = rurl('req_list')

        appstruct = data.__dict__
        del appstruct['_sa_instance_state']
        # appstruct['cou'] = cou
        form = Form(schema,
                    buttons=('submit',),
                    action=action_url,
                    appstruct=appstruct)

        return dict(title=title,
                    action=action_url,
                    form=form,
                    data=appstruct,
                    flash_msg=flash_msg,
                    success=True)


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
    # mailPreferred = ai['mailPreferred']
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

    # import pdb; pdb.set_trace()

    submission = Request(
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
