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
    config.add_route('projects.processors', '/projects/{project_id}/processors')
    config.add_route('projects.collaborators', '/projects/{project_id}/collaborators')
    config.add_route('projects.userprojects', '/users/{user_id}/projects')
    config.add_route('projects', '/projects*extension')
    
    config.add_route('accounts', '/accounts*extension')
    config.add_route('users', '/users*extension')
    
    config.add_route('camera_models', '/camera_models*extension')
    config.add_route('manufactories.list','/manufactories')
    config.add_route('manufactories', '/manufactories/{manufactory_id}')
    config.add_route('manufactories.models', '/manufactories/{manufactory_id}/models')
    
    #co_user
    config.add_route('users.list_users', '/co_users/users')
    config.add_route('users.show_users', '/co_users/users/{user_id}')
    
    #cameras
    config.add_route('cameras.operating', '/cameras/{camera_id}/operating')
    config.add_route('cameras.image_processor', '/cameras/{camera_id}/processors')
    config.add_route('cameras.status', '/cameras/{camera_id}/status')
    config.add_route('cameras.owner', '/cameras/{camera_id}/owner')
    config.add_route('cameras', '/cameras*extension')
    
    # processor
    config.add_route('processors.processors', '/processors/{processor_id}')
    config.add_route('processors.create_list', '/processors')
    
    # image processor
    config.add_route('image_processors', '/image_processors')
    
    # storage
    config.add_route('storage.download', '/storage/download/{token}{extension:.*}')
    config.add_route('storage', '/storage{extension:.*}')
    
    # admin
    config.add_route('admin.users.list', '/admin/users')
    config.add_route('admin.users', '/admin/users/{user_id}')
    config.add_route('admin.users.users_status', '/admin/users/status/{status_name}')
    config.add_route('admin.users.set_status', '/admin/users/{user_id}/status/{status_name}')

    config.add_route('admin.cameras.list', '/admin/cameras')
    config.add_route('admin.cameras', '/admin/cameras/{camera_id}')
    config.add_route('admin.cameras.operating', '/admin/cameras/{camera_id}/operating')
    
    config.add_route('admin.command_queue.list', '/admin/camera_command_queue')
    config.add_route('admin.command_queue', '/admin/camera_command_queue/{command_id}')

    config.add_route('admin.command_log.list', '/admin/command_log')
    config.add_route('admin.command_log', '/admin/command_log/{command_id}')
    
    config.add_route('admin.compute_nodes.list', '/admin/compute_nodes')
    config.add_route('admin.compute_nodes', '/admin/compute_nodes/{compute_node_id}')
    
    config.add_route('admin.camera_running_fail.list', '/admin/camera_running_fail')
    config.add_route('admin.camera_running_fail', '/admin/camera_running_fail/{compute_node_id}')
    
    
