'''
Created on Jan 3, 2013

@author: ww
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='projects.processors', renderer="json", permission="authenticated")
class ProjectProcessorView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        project_id = matchdict.get('project_id')
        
        project = models.Project.objects(id=project_id).first()
        
        processors = models.Processor.objects(project=project, status='active').order_by("+name").all() 

        result = dict(
                      processors=[dict(id=processor.id, name=processor.name) for processor in processors]
                    )
                      
        return result
