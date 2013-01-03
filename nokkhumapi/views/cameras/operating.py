'''
Created on Dec 26, 2012

@author: ww
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models
@view_defaults(route_name='cameras.operating', renderer="json", permission="authenticated")
class CamearaOperating(object):
    def __init__(self, request):
        self.request = request
    
    @view_config(request_method='POST')
    def operate(self):
        matchdict   = self.request.matchdict
        camera_id = matchdict['camera_id']
    
        camera = models.Camera.objects(owner=self.request.user, id=camera_id).first()
        
        if not camera:
            self.request.response.status = '404 Not Found'
            return {'result':"camera not found id: %s"%camera_id}
        
        operating = self.request.json_body["camera_operating"]["action"]
        command_action  = 'No-command'
        user_command    = 'Undefine'
        if operating == 'start':
            command_action = 'Start'
            user_command = 'Run'
        elif operating == 'stop':
            command_action = 'Stop'
            user_command = 'Suspend'
        
        ccq = models.CameraCommandQueue.objects(owner=self.request.user, camera=camera, action=command_action).first()
        if ccq is not None:
            return Response('Camera name %s on operation' % camera.name)
        
        
        camera.operating.status = command_action
        camera.operating.user_command = user_command
        camera.update_date = datetime.datetime.now()
        camera.save()
        
        ccq         = models.CameraCommandQueue()
        ccq.command_date = datetime.datetime.now()
        ccq.update_date = datetime.datetime.now()
        ccq.action  = command_action
        ccq.status  = 'Waiting'
        ccq.camera  = camera
        ccq.owner   = self.request.user
        ccq.save()
    
        return {'result':"success"}
    
    
            
        
    
    
    
    
    
