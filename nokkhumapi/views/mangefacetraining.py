'''
Created on Jan 15, 2014

@author: yoschanin.s
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

from os import walk
import shutil

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='facetraining.delimage', renderer="json", permission="authenticated")
class Facetraining(object):
    def __init__(self, request):
        self.request = request
    
    @view_config(request_method='POST')
    def post(self):
        matchdict = self.request.matchdict
        processor_id = matchdict.get('processor_id')
        
        processor = models.Processor.objects(id=processor_id, owner=self.request.user).first()
        
        if not processor:
            self.request.response.status = '404 Not Found'
            return {}
        
        processor.status = 'delete'
        processor.save()
        # processor.delete()
        
        return {}
