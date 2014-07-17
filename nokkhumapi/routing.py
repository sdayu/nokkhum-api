'''
Created on Jun 28, 2012
@author: boatkrap
'''


def admin_include(config):
    # admin
    config.add_route('admin.users.list',
                     '/users')
    config.add_route('admin.users',
                     '/users/{user_id}')
    config.add_route('admin.users.users_status',
                     '/users/status/{status_name}')
    config.add_route('admin.users.set_status',
                     '/users/{user_id}/status/{status_name}')

    config.add_route('admin.cameras.list',
                     '/cameras')
    config.add_route('admin.cameras',
                     '/cameras/{camera_id}')

    config.add_route('admin.processors.list',
                     '/processors')
    config.add_route('admin.processors',
                     '/processors/{processor_id}')
    config.add_route('admin.processors.operating',
                     '/processors/{processor_id}/operating')

    config.add_route('admin.processor_commands.list',
                     '/processor_commands')
    config.add_route('admin.processor_commands',
                     '/processor_commands/{processor_command_id}')

    config.add_route('admin.command_queue.list',
                     '/processor_command_queue')
    config.add_route('admin.command_queue',
                     '/processor_command_queue/{command_id}')

    config.add_route('admin.command_log.list',
                     '/command_log')
    config.add_route('admin.command_log',
                     '/command_log/{command_id}')

    config.add_route('admin.compute_nodes.list',
                     '/compute_nodes')
    config.add_route('admin.compute_nodes',
                     '/compute_nodes/{compute_node_id}')
    config.add_route('admin.compute_nodes.vm',
                     '/compute_nodes/{compute_node_id}/vm')
    config.add_route('admin.compute_nodes.processors',
                     '/compute_nodes/{compute_node_id}/processors')

    config.add_route('admin.processor_running_fail.list',
                     '/processor_running_fail')
    config.add_route('admin.processor_running_fail',
                     '/processor_running_fail/{log_id}')

    # administration cache manager
    config.add_route('admin.cache', '/cache')


def add_routes(config):
    config.add_route('index', '/')

    # authentication
    config.add_route('authentications.tokens',
                     '/authentication/tokens')

    config.add_route('notifications.number',
                     '/notifications/number')
    config.add_route('notifications',
                     '/notifications*extension')

    # need to be discussion
    config.add_route('facetraining.delimage',
                     '/mfacetraining/{processor_id}')
    config.add_route('facetraining',
                     '/facetraining*extension')

    config.add_route('projects.acamera',
                     '/projects/{project_id}/cameras/${camera_id}')
    config.add_route('projects.cameras',
                     '/projects/{project_id}/cameras')
    config.add_route('projects.permissions',
                     '/projects/{project_id}/permissions/{user_id}')
    config.add_route('projects.processors',
                     '/projects/{project_id}/processors')
    config.add_route('projects.collaboration',
                     '/projects/{project_id}/collaboration')
    config.add_route('projects.collaborators',
                     '/projects/{project_id}/collaborators')
    config.add_route('projects.userprojects',
                     '/users/{user_id}/projects')
    config.add_route('projects',
                     '/projects*extension')

    config.add_route('forums',
                     '/forums*extension')

    config.add_route('groups.processors',
                     '/groups/{group_id}/processors')
    config.add_route('groups.collaborators',
                     '/groups/{group_id}/collaborators')
    config.add_route('groups.usergroups',
                     '/users/{user_id}/groups')
    config.add_route('groups',
                     '/groups*extension')

    config.add_route('accounts',
                     '/accounts*extension')

    config.add_route('users',
                     '/users*extension')

    config.add_route('camera_models',
                     '/camera_models*extension')
    config.add_route('manufactories.list',
                     '/manufactories')
    config.add_route('manufactories',
                     '/manufactories/{manufactory_id}')
    config.add_route('manufactories.models',
                     '/manufactories/{manufactory_id}/models')

    # co_user
    config.add_route('users.list_users',
                     '/co_users/users')
    config.add_route('users.show_users',
                     '/co_users/users/{user_id}')

    # cameras
    config.add_route('cameras.image_processor',
                     '/cameras/{camera_id}/processors')
    config.add_route('cameras.status',
                     '/cameras/{camera_id}/status')
    config.add_route('cameras.owner',
                     '/cameras/{camera_id}/owner')
    config.add_route('cameras',
                     '/cameras/{camera_id}')
    config.add_route('cameras.create_list',
                     '/cameras')

    # processor
    config.add_route('processors.processors',
                     '/processors/{processor_id}')
    config.add_route('processors.create_list',
                     '/processors')
    config.add_route('processors.cameras',
                     '/processors/{processor_id}/cameras')
    config.add_route('processors.operating',
                     '/processors/{processor_id}/operating')

    # user_resource
    config.add_route('user_resource',
                     '/user_resources/{processor_id}')
    # billing
    config.add_route('billing.users',
                     '/billing/processors/{processor_id}')
    config.add_route('billing.billing_cycle',
                     '/billing/processors/{processor_id}/cycle')

    config.add_route('billing.service_plans.create_list',
                     '/billing/service_plans')
    config.add_route('billing.service_plans',
                     '/billing/service_plans/{service_plan_id}')
    config.add_route('billing.default_service_plans',
                     '/billing/service_plans/{service_plan_id}/default')

    # image processor
    config.add_route('image_processors',
                     '/image_processors')

    # storage
    config.add_route('storage.download',
                     '/storage/download/{token}{extension:.*}')
    config.add_route('storage',
                     '/storage{extension:.*}')

    # administrator route
    config.include(admin_include,
                   route_prefix='/admin')
