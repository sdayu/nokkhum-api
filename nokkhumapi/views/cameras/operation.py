'''
Created on Dec 26, 2012

@author: ww
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models
@view_config(route_name='camera.camera_operating',renderer="json", permission="authenticated")
class Operating(object):
    def __init__(self, request):
        self.request = request
        
    def operating(self):
        matchdict   = self.request.matchdict
        camera_id = matchdict['camera_id']
        
        
    
        camera = models.Camera.objects(owner=request.user, id=camera_id).first()
        
        if not camera:
            self.request.response.status = '404 Not Found'
            return {'result':"not found id: %d"%id}
        
        command_action  = 'No-command'
        user_command    = 'Undefine'
        if operating == 'start':
            command_action = 'Start'
            user_command = 'Run'
        elif operating == 'stop':
            command_action = 'Stop'
            user_command = 'Suspend'
        
        ccq = models.CameraCommandQueue.objects(owner=request.user, camera=camera, action=command_action).first()
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
        ccq.owner   = request.user
        ccq.save()
    
        return HTTPFound(location=request.route_path('project_index', name=camera.project.name))
    
    
            
        
    
    
    
    
    