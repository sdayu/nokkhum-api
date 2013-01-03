'''
Created on Jun 28, 2012

@author: boatkrap
'''

def add_routes(config):
    config.add_route('index', '/')
    
    #authentication
    config.add_route('authentications.tokens', '/authentication/tokens')
    
    config.add_route('projects.cameraproject', '/cameras/{camera_id}/project')
    config.add_route('projects.userprojects', '/users/{user_id}/projects')
    # camera
    config.add_route('cameras', '/cameras*extension')
    config.add_route('users', '/users*extension')
    config.add_route('projects', '/projects*extension')
    config.add_route('accounts', '/accounts*extension')
    config.add_route('camera_models', '/camera_models*extension')
    config.add_route('manufactories','/manufactories')
    config.add_route('cameras.operating', '/camera/{camera_id}/operating')
    config.add_route('cameras.image_processor', '/camera/image_processor')
#    config.add_route('cameras_post', '/cameras')
#    config.add_route('cameras_get', '/cameras/{id}')
#    config.add_route('cameras_delete', '/cameras/{id}')