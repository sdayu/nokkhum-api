'''
Created on 12 Jan 2013

@author: ww
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models
@view_defaults(route_name='cameras.status', renderer="json", permission="authenticated")
class CamearaStatus(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        camera_id = matchdict.get('camera_id')

        
        camera = models.Camera.objects(id=camera_id).first()
        if not camera:
            self.request.response.status = '404 Not Found'
            return {}
        result = {}   
        result["camera"] = dict(
                                id=camera.id,
                                status=camera.status
                                
                
                                
                                )
        self.request.response.headers['Access-Control-Allow-Origin'] = '*'
        return result