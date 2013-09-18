from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.security import authenticated_userid
from nokkhumapi import models

@view_defaults(route_name='admin.cameras', permission='role:admin', renderer='json')
class Camera:
    def __init__(self, request):
        self.request = request
        
    def build_camera_result(self, camera):
        result = dict(
                   dict(
                        id= camera.id,
                        username=camera.username,
                        password=camera.password,
                        name=camera.name,
                        host=camera.host,
                        port=camera.port,
                        video_url=camera.video_url,
                        audio_url=camera.audio_url,
                        image_url=camera.image_url,
                        image_size=camera.image_size,
                        fps=camera.fps,
                        status=camera.status,
                        create_date=camera.create_date,
                        update_date=camera.update_date,
                        project=dict(
                                id=camera.project.id,
                                name=camera.project.name
                                ),
                        model=dict(
                                id=camera.camera_model.id, 
                                name=camera.camera_model.name, 
                                manufactory=dict(
                                            id=camera.camera_model.manufactory.id, 
                                            name=camera.camera_model.manufactory.name
                                            )
                                ),
                        owner=dict(
                                   id=camera.owner.id,
                                   email=camera.owner.email
                                   )
                        )
                      
            )
        
        return result
        
    @view_config(route_name='admin.cameras.list')
    def list_camera(self):
        return dict(
                    cameras= [self.build_camera_result(camera)
                              for camera in models.Camera.objects().order_by("+id").all()]
                    )
        
    @view_config(request_method="GET")
    def get(self):
        matchdict = self.request.matchdict
        camera_id = matchdict.get('camera_id')
        camera= models.Camera.objects(id=camera_id).first()
        
        if not camera:
            self.request.response.status = '404 Not Found'
            return {}
        
        result = dict(
                      camera=self.build_camera_result(camera)
                      )
        return result