from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.security import authenticated_userid

from nokkhumapi import models


@view_defaults(route_name='admin.command_queue', permission='r:admin', renderer='json')
class CameraCommandQueue:
    def __init__(self, request):
        self.request = request
    
    @view_config(route_name='admin.command_queue.list', permission='r:admin', renderer='json', request_method="GET")
    def list_command(self):
        camera_command_queue = models.CameraCommandQueue.objects().order_by("+id").all()
        return dict(
                    camera_command_queue=[dict(
                                               id=command.id,
                                               camera=dict(
                                                           id=command.camera.id
                                                           ),
                                               owner=dict(
                                                          id=command.owner.id,
                                                          email=command.owner.email
                                                          ),
                                               action=command.action,
                                               status=command.status,
                                               command_date=command.command_date,
                                               update_date=command.update_date
                                               )
                                          for command in camera_command_queue]
                    )
        
        
    @view_config(request_method="GET")
    def get(self):
        matchdict = self.request.matchdict
        command_id = matchdict['command_id']
        command = models.CameraCommandQueue.objects().with_id(command_id)
        return dict(
                    camera_command=dict(
                                        id=command.id,
                                        action=command.action,
                                        status=command.status,
                                        command_date=command.command_date,
                                        update_date=command.update_date,
                                        message=command.message,
                                        camera=dict(
                                                   id=command.camera.id
                                                   ),
                                       owner=dict(
                                                  id=command.owner.id,
                                                  email=command.owner.email
                                                  ),
                                        )
                    )