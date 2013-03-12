'''
Created on Jun 28, 2012

@author: boatkrap
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='cameras.owner', renderer="json", permission="authenticated")
class CameraOwnerView(object):
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        camera_id = matchdict.get('camera_id')
        
        if id.isdigit():
            camera = models.Camera.objects(id=camera_id, owner=self.request.user).first()
        else:
            camera = models.Camera.objects(name=camera_id, owner=self.request.user).first()
        
        if not camera:
            self.request.response.status = '404 Not Found'
            return {}
        
        result = dict(
                      owner=dict(
                            id= camera.owner.id,
                            email=camera.owner.email
                            )
                      )
        return result


    