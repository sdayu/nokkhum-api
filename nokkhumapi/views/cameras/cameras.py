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
        id = int(extension[0])
        
        camera = models.Camera.objects(id=id).first()
        
        if not camera:
            self.request.response.status = '404 Not Found'
            return {}
        
        result = {"camera":{}}
        result["camera"]["id"] = camera.id
        result["camera"]["username"] = camera.username
        result["camera"]["password"] = camera.password
        result["camera"]["name"] = camera.name
        result["camera"]["url"] = camera.url
        result["camera"]["image_size"] = camera.image_size
        result["camera"]["fps"] = camera.fps
        result["camera"]["status"] = camera.status
        result["camera"]["storage_periods"] = camera.storage_periods
        result["camera"]["create_date"] = camera.create_date
        result["camera"]["processors"] = camera.processors
        result["camera"]["model"] = dict(id=camera.camera_model.id, 
                                         name=camera.camera_model.name, 
                                         manufactory=dict(
                                                id=camera.camera_model.manufactory.id, 
                                                name=camera.camera_model.manufactory.name))
        self.request.response.headers['Access-Control-Allow-Origin'] = '*'        
        return result

    @view_config(request_method='POST')
    def create(self):
#        camera_dict = json.loads(self.request.json_body)["camera"]
        camera_dict = self.request.json_body["camera"]
        
        camera          = models.Camera()
        camera.name     = camera_dict["name"]
        camera.username = camera_dict["username"]
        camera.password = camera_dict["password"]
        camera.image_size   = camera_dict["image_size"]
        camera.fps      = camera_dict["fps"]
        camera.storage_periods = camera_dict["storage_periods"]
        camera.create_date  = datetime.datetime.now()
        
        camera.owner    = models.User.objects(id=camera_dict["user"]["id"]).first()
        camera.operating = models.CameraOperating()
        camera.project  = models.Project.objects(id=camera_dict["project"]["id"]).first()
        camera.processors = camera_dict.get('processors', [])
        camera.camera_model   = models.CameraModel.objects(id=camera_dict["model"]["id"]).first()
        
        if len(camera_dict["url"]) == 0:
            
            if camera.camera_model.name.lower() != "opencv":
            
                from nokkhumapi.driver.camera import factory
                fac = factory.CameraDriverFactory(camera.camera_model.manufactory.name)
                camera.url = fac.get_driver(camera.camera_model.name, camera.__dict__)
            
        if camera.url is None:
            camera.url      = camera_dict["url"]
        
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
        camera.username = camera_dict["username"]
        camera.password = camera_dict["password"]
        camera.image_size   = camera_dict["image_size"]
        camera.fps      = camera_dict["fps"]
        camera.storage_periods = camera_dict["storage_periods"]
        if camera_dict.get('processors'):
            camera.processors = camera_dict.get('processors')
        camera.camera_model    = models.CameraModel.objects(id=camera_dict["model"]["id"]).first()
        
        if len(camera_dict["url"]) == 0:
            if camera.camera_model.name.lower() != "opencv":
                from nokkhumapi.driver.camera import factory
                fac = factory.CameraDriverFactory(camera.camera_model.manufactory.name)
                camera.url = fac.get_driver(camera.camera_model.name, camera.__dict__)
            
        else:
            camera.url      = camera_dict["url"]
        
        camera.save()

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
        self.request.response.headers['Access-Control-Allow-Origin'] = '*'
        return {'message':"delete success"}
    