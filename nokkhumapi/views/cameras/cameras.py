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
        extension = matchdict.get('extension')
        id = extension[0]
        
        if id.isdigit():
            camera = models.Camera.objects(id=id, owner=self.request.user).first()
        else:
            camera = models.Camera.objects(name=id, owner=self.request.user).first()
        
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
                            video_url=camera.video_url,
                            audio_url=camera.audio_url,
                            image_url=camera.image_url,
                            image_size=camera.image_size,
                            fps=camera.fps,
                            status=camera.status,
                            storage_periods=camera.storage_periods,
                            create_date=camera.create_date,
                            update_date=camera.update_date,
                            image_processors=camera.processors,
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
                                    )
                            )
                      )
        return result

    @view_config(request_method='POST')
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
        camera.storage_periods = camera_dict["storage_periods"]
        camera.create_date  = datetime.datetime.now()
        
        camera.owner    = models.User.objects(id=camera_dict["user"]["id"]).first()
        camera.operating = models.CameraOperating()
        camera.project  = models.Project.objects(id=camera_dict["project"]["id"]).first()
        camera.processors = camera_dict.get('image_processors', [])
        camera.camera_model   = models.CameraModel.objects(id=camera_dict["model"]["id"]).first()

        if camera.camera_model.name.lower() != "opencv":
            from nokkhumapi.driver.camera import factory
            fac = factory.CameraDriverFactory().get_camera_driver(camera.camera_model.manufactory.name)
            camera_driver = fac.get_driver(camera.camera_model.name, **camera_dict)
            camera.video_url = camera_driver.get_video_url(extension="?.mjpg")
            camera.audio_url = camera_driver.get_audio_url()
            camera.image_url = camera_driver.get_image_url()
            
        if camera.video_url is None:
            camera.video_url      = camera_dict["video_url"]
        
        camera.save()
        
        result = {"camera":camera_dict}
        result["camera"]["id"] = camera.id
        return result
    
    @view_config(request_method='PUT')
    def update(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        id = int(extension[0])
        
        camera = models.Camera.objects(id=id).first()
        if not camera:
            self.request.response.status = '404 Not Found'
            return {'message':"not found id: %d"%id}
        
        camera_dict = self.request.json_body["camera"]
        
        camera.name     = camera_dict["name"]
        camera.host     = camera_dict['host']
        camera.port     = camera_dict['port']
        camera.username = camera_dict["username"]
        camera.password = camera_dict["password"]
        camera.image_size   = camera_dict["image_size"]
        camera.fps      = camera_dict["fps"]
        camera.storage_periods = camera_dict["storage_periods"]
        if camera_dict.get('image_processors', None):
            camera.processors = camera_dict.get('image_processors')
        camera.camera_model    = models.CameraModel.objects(id=camera_dict["model"]["id"]).first()
        
        if camera.camera_model.name.lower() != "opencv":
            from nokkhumapi.driver.camera import factory
            fac = factory.CameraDriverFactory().get_camera_driver(camera.camera_model.manufactory.name)
            camera_driver = fac.get_driver(camera.camera_model.name, **camera_dict)
            camera.video_url = camera_driver.get_video_url(extension="?.mjpg")
            camera.audio_url = camera_driver.get_audio_url()
            camera.image_url = camera_driver.get_image_url()
            
        else:
            camera.url      = camera_dict["video_url"]
        
        camera.save()

        camera_dict['video_url'] = camera.video_url
        camera_dict['audio_url'] = camera.audio_url
        camera_dict['image_url'] = camera.image_url
        return {'camera':camera_dict}

    @view_config(request_method='DELETE')
    def delete(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        id = int(extension[0])
        
        camera = models.Camera.objects(id=id).first()
        if not camera:
            self.request.response.status = '404 Not Found'
            return {'message':"not found id: %d"%id}
        
        camera.delete()
        return {'message':"delete success"}
    