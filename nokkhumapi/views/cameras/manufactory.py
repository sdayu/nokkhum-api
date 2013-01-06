'''
Created on Dec 25, 2012

@author: ww
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models
@view_defaults(route_name='manufactories', renderer="json")
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