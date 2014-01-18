'''
Created on Jan 15, 2014

@author: yoschanin.s
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='facetraining', renderer="json", permission="authenticated")
class Facetraining(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        
        cameras = models.Camera.objects(owner=self.request.user).all()
        number = 0
        for camera in cameras:
            notifications = models.Notification.objects(camera=str(camera.id),status='False').all()
            number += len(notifications) 
                
        result = dict(
                      number=number
                    )
        
        return result

