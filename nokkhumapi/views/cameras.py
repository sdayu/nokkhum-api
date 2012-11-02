'''
Created on Jun 28, 2012

@author: boatkrap
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from .. import models

@view_defaults(route_name='cameras', renderer="json")
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
        
        return result

    @view_config(request_method='POST')
    def create(self):
#        camera_dict = json.loads(self.request.json_body)["camera"]
        camera_dict = self.request.json_body["camera"]
        
        camera          = models.Camera()
        camera.name     = camera_dict["name"]
        camera.username = camera_dict["username"]
        camera.password = camera_dict["password"]
        camera.url      = camera_dict["url"]
        camera.image_size   = camera_dict["image_size"]
        camera.fps      = camera_dict["fps"]
        camera.storage_periods = camera_dict["storage_periods"]
        camera.create_date  = datetime.datetime.now()
        
        camera.owner    = models.User.objects(id=1).first()
        camera.operating = models.CameraOperating()
        camera.project  = models.Project.objects(id=1).first()
        camera.camera_model    = models.CameraModel.objects()[0]
        
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
            return {'result':"not found id: %d"%id}
        
        camera_dict = self.request.json_body["camera"]
        
        camera.name     = camera_dict["name"]
        camera.username = camera_dict["username"]
        camera.password = camera_dict["password"]
        camera.url      = camera_dict["url"]
        camera.image_size   = camera_dict["image_size"]
        camera.fps      = camera_dict["fps"]
        camera.storage_periods = camera_dict["storage_periods"]
        
        camera.save()

        return {'result':camera_dict}

    @view_config(request_method='DELETE')
    def delete(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        id = int(extension[0])
        
        camera = models.Camera.objects(id=id).first()
        if not camera:
            self.request.response.status = '404 Not Found'
            return {'result':"not found id: %d"%id}
        
        camera.delete()

        return {'result':"delete success"}
    