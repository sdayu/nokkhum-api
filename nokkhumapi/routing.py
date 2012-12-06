'''
Created on Jun 28, 2012

@author: boatkrap
'''

def add_routes(config):
    config.add_route('index', '/')
    
    #authentication
    config.add_route('authentications.tokens', '/authentication/tokens')
    
    # camera
    config.add_route('cameras', '/cameras*extension')
    config.add_route('users', '/users*extension')
    config.add_route('projects', '/projects*extension')
    config.add_route('accounts', '/accounts*extension')
#    config.add_route('cameras_post', '/cameras')
#    config.add_route('cameras_get', '/cameras/{id}')
#    config.add_route('cameras_delete', '/cameras/{id}')