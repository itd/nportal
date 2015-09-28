from pyramid.response import Response
from pyramid.decorator import reify
#from pyramid import request
from pyramid.renderers import render_to_response
# from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
import deform
# from deform import (decorator, default_renderer, field, form, widget)
from nportal.models import (
    DBSession,
    SiteModel,
    UserAccountModel
)


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_nportal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


class BaseViews(object):
    """
    The base views, such as home, login, logout, etc.
    """
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("../templates/_layout.pt")
        self.layout = renderer.implementation().macros['layout']

    # @reify
    # def reqts(self):
    #     return self.home_fform.get_widget_resources()

    #    @reify
    #    def home(self):
    #        schema = HomePage()
    #        return deform.Form(schema, buttons=('submit',))

    @reifyx
    def changepass(self):
        schema = UserAccountModel()
        return deform.Form(schema, buttons=('submit',))

    # @view_config(route_name='home', renderer='../templates/home.pt')
    @view_config(route_name='home', renderer='../templates/home.pt')
    def home_view(self):
        request = self.request
        #pagename = request.matchdict['pagename']
        try:
            one = DBSession.query(SiteModel).filter(
                SiteModel.name == 'one').first()
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain',
                            status_int=500)

        import pdb; pdb.set_trace()

        return {'one': one,
                'project': 'nportal',
                }
# 'request_user_account_url': request.route_url('request_user_account')
