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
    @view_config(request_method='PUT')
    def operate(self):
        matchdict   = self.request.matchdict
        camera_id = matchdict['camera_id']
    
        camera = models.Camera.objects(owner=self.request.user, id=camera_id).first()
        
        if not camera:
            self.request.response.status = '404 Not Found'
            return {'result':"camera not found id: %s"%camera_id}
        
        operating = self.request.json_body["camera_operating"]["action"]
        command_action  = 'no-command'
        user_command    = 'undefined'
        if operating == 'start':
            command_action = 'start'
            user_command = 'run'
        elif operating == 'stop':
            command_action = 'stop'
            user_command = 'suspend'
        
        ccq = models.CameraCommandQueue.objects(owner=self.request.user, camera=camera, action=command_action).first()
        if ccq is not None:
            self.request.response.status = '406 Not Acceptable'
            return {'result':'camera name %s on operation' % camera.id}

        
        camera.operating.status = command_action
        camera.operating.user_command = user_command
        camera.update_date = datetime.datetime.now()
        camera.save()
        
        ccq         = models.CameraCommandQueue()
        ccq.command_date = datetime.datetime.now()
        ccq.update_date = datetime.datetime.now()
        ccq.action  = command_action
        ccq.status  = 'waiting'
        ccq.camera  = camera
        ccq.owner   = self.request.user
        ccq.save()
        print("update success")

        return dict(
                    camera_operating=dict(
                           action=ccq.action,
                           id=ccq.id,
                           status=ccq.status,
                           camera=dict(
                                     id=ccq.camera.id                      
                                     ),
                            user=dict(
                                    id=ccq.owner.id
                                    )
                           ),
                    result="success"
                )
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        camera_id = matchdict.get('camera_id')

        camera = models.Camera.objects(id=camera_id).first()

        if not camera:
            self.request.response.status = '404 Not Found'
            return {}
        result = dict(
                      camera_operating=dict(
                            status=camera.operating.status, 
                            update_date=camera.operating.update_date,
                            user_command=camera.operating.user_command,
#                                         compute_node={'id':camera.operating.compute_node._id}
                                
                            )
                      )
        
        return result
            
        
    
    
    
    
    
