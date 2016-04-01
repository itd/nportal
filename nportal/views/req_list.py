from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import (scoped_session, sessionmaker)

from pyramid.view import view_config
from pyramid.renderers import get_renderer


from nportal.models import (
    DBSession,
    Requests,
    CountryCodes,
    # Citizenship
    )


# sqlalchemy setup
# DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),
#                                         expire_on_commit=False))


def site_layout():
    renderer = get_renderer("../templates/_layout_admin.pt")
    layout = renderer.implementation().macros['layout']
    return layout


def add_base_template(event):
    base = get_renderer('templates/_layout.pt').implementation()
    event.update({'base': base})


class AdminViews(object):
    """
    """
    def __init__(self, request):
        self.request = request
        # renderer = get_renderer("../templates/_layout.pt")
        # self.layout = renderer.implementation().macros['layout']
        self.layout = site_layout()
        self.title = "Request Admin Views"

    @view_config(route_name='req_list',
                 renderer='../templates/req_list.pt',
                 permission='view')
    def req_list(self):
        """
        Path is /radmin/req
        """
        title = "Request List"
        sess = DBSession()
        users = sess.query(Requests).order_by(Requests.sn).all()
        users = [u.__dict__ for u in users]
        citz = sess.query(Requests).order_by(Requests.sn).all()

        return dict(title=title,
                    page_title=title,
                    users=users)
