from pyramid.config import Configurator
from sqlalchemy import engine_from_config

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
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')


    #config.add_route('login', '/login')
    #config.add_route('logout', '/logout')

    config.add_renderer('jsonp', JSONP(param_name='callback'))
    config.add_renderer(name='csv',
                        factory='allocations.views.CSVRenderer')

    # views
    # config.add_static_view('static', 'static', cache_max_age=1)
    # config.add_static_view('static', 'nportal:static/', cache_max_age=1)
    config.add_static_view('deform', 'deform:static')
    config.add_static_view('static', 'static', cache_max_age=1)  ## 3600

    config.add_route('home', '/')
    config.add_route('changepass', '/changepass')

    config.scan()
    return config.make_wsgi_app()
