'''
Created on Sep 14, 2013

@author: boatkrap
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='processors.cameras', renderer="json", permission="authenticated")
class ProcessorCameraView(object):
    def __init__(self, request):
        self.request = request
    
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        processor_id = matchdict.get('processor_id')
        
        processor = models.Processor.objects(id=processor_id).first()
        
        result = dict(
                      cameras=[dict(id=camera.id, name=camera.name) for camera in processor.cameras]
                      )
        return result