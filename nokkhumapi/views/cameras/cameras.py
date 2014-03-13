'''
Created on Jun 28, 2012

@author: boatkrap
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='cameras', renderer="json", permission="authenticated")
class CameraView(object):
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        camera_id = matchdict.get('camera_id')
        
        camera = models.Camera.objects(id=camera_id, owner=self.request.user).order_by("+name").first()
        
        if not camera:
            self.request.response.status = '404 Not Found'
            return {}
        
        result = dict(
                      camera=dict(
                            id= camera.id,
                            username=camera.username,
                            password=camera.password,
                            name=camera.name,
                            host=camera.host,
                            port=camera.port,
                            video_uri=camera.video_uri,
                            audio_uri=camera.audio_uri,
                            image_uri=camera.image_uri,
                            image_size=camera.image_size,
                            fps=camera.fps,
                            created_date=camera.created_date,
                            updated_date=camera.updated_date,
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
                                       ),
                            location=camera.location
                            )
                      )
        return result

    @view_config(route_name='cameras.create_list', request_method='POST')
    def create(self):
#        camera_dict = json.loads(self.request.json_body)["camera"]
        camera_dict = self.request.json_body["camera"]
        
        camera          = models.Camera()
        camera.name     = camera_dict["name"]
        camera.host     = camera_dict['host']
        camera.port     = camera_dict['port']
        camera.username = camera_dict["username"]
        camera.password = camera_dict["password"]
        camera.image_size   = camera_dict["image_size"]
        camera.fps      = camera_dict["fps"]
        camera.created_date  = datetime.datetime.now()
        
        camera.owner    = self.request.user
        camera.project  = models.Project.objects(id=camera_dict["project"]["id"]).first()
        camera.camera_model   = models.CameraModel.objects(id=camera_dict["model"]["id"]).first()
        
        camera.location = camera_dict['location']

        if camera.camera_model.name.lower() != "opencv":
            from nokkhumapi.driver.camera import factory
            fac = factory.CameraDriverFactory().get_camera_driver(camera.camera_model.manufactory.name)
            camera_driver = fac.get_driver(camera.camera_model.name, **camera_dict)
            camera.video_uri = camera_driver.get_video_uri()
            camera.audio_uri = camera_driver.get_audio_uri()
            camera.image_uri = camera_driver.get_image_uri()
            
        if camera.video_uri is None:
            camera.video_uri      = camera_dict["video_uri"]
        
        camera.save()
        
        result = {"camera":camera_dict}
        result["camera"]["id"] = camera.id
        return result
    
    @view_config(request_method='PUT')
    def update(self):
        matchdict = self.request.matchdict
        camera_id = matchdict.get('camera_id')
        
        camera = models.Camera.objects(id=camera_id).first()
        if not camera:
            self.request.response.status = '404 Not Found'
            return {'message':"not found id: %d"%camera_id}
        
        camera_dict = self.request.json_body["camera"]
        
        camera.name     = camera_dict["name"]
        camera.host     = camera_dict['host']
        camera.port     = camera_dict['port']
        camera.username = camera_dict["username"]
        camera.password = camera_dict["password"]
        camera.image_size   = camera_dict["image_size"]
        camera.fps      = camera_dict["fps"]
        camera.camera_model    = models.CameraModel.objects(id=camera_dict["model"]["id"]).first()
        
        camera.location = camera_dict['location']
        
        if camera.camera_model.name.lower() != "opencv":
            from nokkhumapi.driver.camera import factory
            fac = factory.CameraDriverFactory().get_camera_driver(camera.camera_model.manufactory.name)
            camera_driver = fac.get_driver(camera.camera_model.name, **camera_dict)
            camera.video_uri = camera_driver.get_video_uri()
            camera.audio_uri = camera_driver.get_audio_uri()
            camera.image_uri = camera_driver.get_image_uri()
            
        else:
            camera.url      = camera_dict["video_uri"]
        
        camera.save()

        camera_dict['video_uri'] = camera.video_uri
        camera_dict['audio_uri'] = camera.audio_uri
        return {'camera':camera_dict}

    @view_config(request_method='DELETE')
    def delete(self):
        matchdict = self.request.matchdict
        camera_id = matchdict.get('camera_id')
        
        camera = models.Camera.objects(id=camera_id).first()
        if not camera:
            self.request.response.status = '404 Not Found'
            return {'message':"not found id: %d"%id}
        
        camera.delete()
        return {'message':"delete success"}
    