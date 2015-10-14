from pyramid.config import Configurator
from pyramid.renderers import JSONP

from sqlalchemy import engine_from_config
from pyramid.session import SignedCookieSessionFactory

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    req_session_factory = SignedCookieSessionFactory('somerandomstringforthereq')
    config = Configurator(settings=settings,
                          session_factory=req_session_factory)
    config.include('pyramid_chameleon')

    #config.add_route('login', '/login')
    #config.add_route('logout', '/logout')

    config.add_renderer('jsonp', JSONP(param_name='callback'))
    config.add_renderer(name='csv',
                        factory='nportal.views.CSVRenderer')

    # views
    config.add_static_view('static', 'static', cache_max_age=1)
    config.add_static_view('deform', 'deform:static')
    #config.add_static_view('static', 'static', cache_max_age=1)  ## 3600

    config.add_route('home', '/')
    config.add_route('changepass', '/changepass')
    config.add_route('request_user_account', '/request_user_account')
    config.add_route('request_received_view', '/request_received')

    config.scan()
    return config.make_wsgi_app()
