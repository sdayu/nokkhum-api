'''
Created on Dec 25, 2012

@author: ww
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models
@view_defaults(route_name='camera_models', renderer="json", permission="authenticated")
class CameraModels(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        id = extension[0]
        manufactory = models.Manufactory.objects(id=id).first()
        camera_models = models.CameraModel.objects(manufactory=manufactory).all()

        result = {"camera_models":[dict(id=camera_model.id, name=camera_model.name) for camera_model in camera_models]
                  }
        
        
        return result