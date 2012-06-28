from pyramid.config import Configurator

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    
    from .routing import add_routes
    add_routes(config)
    
    config.scan()
    
    from .models import initial
    initial(config.registry.settings)
    
    modify_json_renderer(config)
    
    return config.make_wsgi_app()


def modify_json_renderer(config):
    from pyramid.renderers import JSON
    import datetime
    
    json_renderer = JSON()
    def datetime_adapter(obj, request):
        return obj.isoformat()
    
    json_renderer.add_adapter(datetime.datetime, datetime_adapter)
    
    # then during configuration ....
    config.add_renderer('json', json_renderer)
