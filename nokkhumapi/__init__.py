from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    from nokkhumapi.security import TokenAuthenticationPolicy
    authn_policy =  TokenAuthenticationPolicy()
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, root_factory='nokkhumapi.acl.RootFactory',
                          authentication_policy=authn_policy, authorization_policy=authz_policy)
    
    from .routing import add_routes
    add_routes(config)
    
    config.scan('nokkhumapi.views')
    
    from .models import initial
    initial(config.registry.settings)
    
    modify_json_renderer(config)
    
    from .security import SecretManager, RequestWithUserAttribute
    
    config.set_request_factory(RequestWithUserAttribute)
    secret_manager = SecretManager(settings.get('nokkhum.auth.secret'))
    config.registry.settings['secret_manager'] = secret_manager
    
    config.add_subscriber(add_response_callback, NewRequest)
    
    return config.make_wsgi_app()


def modify_json_renderer(config):
    from pyramid.renderers import JSON
    import datetime
    from bson import ObjectId
    
    json_renderer = JSON()
    def datetime_adapter(obj, request):
        return obj.isoformat()
    
    def mongo_object_adapter(obj, request):
        return str(obj)
    
    json_renderer.add_adapter(datetime.datetime, datetime_adapter)
    json_renderer.add_adapter(datetime.date, datetime_adapter)
    json_renderer.add_adapter(ObjectId, mongo_object_adapter)
    
    # then during configuration ....
    config.add_renderer('json', json_renderer)
    
def add_response_callback(event):
    
    def set_default_header_callback(request, response):
        response.headers['Access-Control-Allow-Origin'] = '*'
#         response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, x-xsrf-token, Accept'
#         response.headers['Content-Type'] = 'application/json'
        
    event.request.add_response_callback(set_default_header_callback)

