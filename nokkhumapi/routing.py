'''
Created on Jun 28, 2012

@author: boatkrap
'''

def add_routes(config):
    config.add_route('index', '/')
    
    # camera
    config.add_route('cameras', '/cameras*extension')
    config.add_route('users', '/users*extension')
    config.add_route('projects', '/projects*extention')
#    config.add_route('cameras_post', '/cameras')
#    config.add_route('cameras_get', '/cameras/{id}')
#    config.add_route('cameras_delete', '/cameras/{id}')