'''
Created on Jun 28, 2012

@author: boatkrap
'''

def add_routes(config):
    config.add_route('index', '/')
    
    #authentication
    config.add_route('authentications.tokens', '/authentication/tokens')

    config.add_route('projects.acamera', '/projects/{project_id}/cameras/${camera_id}')    
    config.add_route('projects.cameras', '/projects/{project_id}/cameras')
    config.add_route('projects.collaborators', '/projects/{project_id}/collaborators')
    config.add_route('projects.userprojects', '/users/{user_id}/projects')
    config.add_route('projects', '/projects*extension')
    
    config.add_route('accounts', '/accounts*extension')
    config.add_route('users', '/users*extension')
    
    config.add_route('camera_models', '/camera_models*extension')
    config.add_route('manufactories','/manufactories')
    config.add_route('manufactories.models', '/manufactories/{manufactory_id}/models')
    
    #co_user
    config.add_route('users.list_users', '/co_users/users')
    config.add_route('users.show_users', '/co_users/users/{user_id}')
    
    
    #cameras
    config.add_route('cameras.operating', '/cameras/{camera_id}/operating')
    config.add_route('cameras.image_processor', '/cameras/{camera_id}/processors')
    config.add_route('cameras.status', '/cameras/{camera_id}/status')
    config.add_route('cameras', '/cameras*extension')
    
    #admin
    config.add_route('admin.users.list_users', '/admin/users')
    config.add_route('admin.users.show_users', '/admin/users/{user_id}')
    config.add_route('admin.cameras.list_cameras', '/admin/cameras')
    config.add_route('admin.cameras.show_cameras', '/admin/cameras/{camera_id}')
    config.add_route('admin.users.users_status', '/admin/users/status/{status_name}')
    config.add_route('admin.users.set_status', '/admin/users/{user_id}/status/{status_name}')
#    config.add_route('cameras_post', '/cameras')
#    config.add_route('cameras_get', '/cameras/{id}')
#    config.add_route('cameras_delete', '/cameras/{id}')

    # storage
    config.add_route('storage.download', '/storage/download/{token}{extension:.*}')
    config.add_route('storage', '/storage{extension:.*}')
    
    
