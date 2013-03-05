'''
Created on Dec 25, 2012

@author: ww
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models
@view_defaults(route_name='manufactories', renderer="json", permission="authenticated")
class Manufactory(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        
     
        manufactories = models.Manufactory.objects().all()

        result = {"manufactories":[dict(id=manufactory.id, name=manufactory.name) for manufactory in manufactories]
                  }
        
        return result
    
    @view_config(route_name='manufactories.models', renderer="json", permission="authenticated", request_method='GET')
    def list_model_by_manufactory(self):
        matchdict = self.request.matchdict
        manufactory_id = matchdict.get('manufactory_id')
        manufactory = models.Manufactory.objects(id=manufactory_id).first()
        camera_models = models.CameraModel.objects(manufactory=manufactory).all()

        result = dict(
                      camera_models=[
                            dict(id=camera_model.id, name=camera_model.name) 
                                for camera_model in camera_models]
                  )
        
        return result