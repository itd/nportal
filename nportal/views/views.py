from pyramid.response import Response
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from deform import (decorator, default_renderer, field, form, widget)
from .models import (
    DBSession,
    MyModel,
    )


@view_config(route_name='default', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'nportal'}


# New User Account Request Application Form
# new_user_account_app.pt

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

class AccountViews(object):
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("templates/_layout.pt")
        self.layout = renderer.implementation().macros['layout']

    @reify
    def reqts(self):
        return self.home_form.get_widget_resources()

    @reify
    def home(self):
        schema = HomePage()
        return deform.Form(schema, buttons=('submit',))

    @reify
    def changepass(self):
        schema = UserAccount()
        return deform.Form(schema, buttons=('submit',))
