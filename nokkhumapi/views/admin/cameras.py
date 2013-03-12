from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.security import authenticated_userid
from nokkhumapi import models

@view_defaults(route_name='admin.cameras', permission='r:admin', renderer='json')
class Camera:
    def __init__(self, request):
        self.request = request
        
    @view_config(route_name='admin.cameras.list')
    def list_camera(self):
        return dict(
                    cameras= [dict(
                                   id=camera.id, 
                                   name=camera.name,
                                   owner=dict(
                                              id=camera.owner.id,
                                              email=camera.owner.email
                                              )
                                   )
                              for camera in models.Camera.objects().all()]
                    )
        
    @view_config(request_method="GET")
    def get(self):
        matchdict = self.request.matchdict
        camera_id = int(matchdict['id'])
        camera= models.Camera.objects(id=camera_id).first()
        
        return dict(
                    camera=camera
                    )