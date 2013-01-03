'''
Created on Jan 3, 2013

@author: ww
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models
@view_defaults(route_name='projects.cameraproject', renderer="json", permission="authenticated")
class UserProjectsView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        camera_id = matchdict.get('camera_id')
        
        camera = models.Camera.objects(id=camera_id).first()
        if not camera:
            self.request.response.status = '404 Not Found'
            return {'error':{'message':'This camera not found.'}}
        
        projects = models.Project.objects(owner=camera).all()
        

        result = {"projects":[dict(id=camera.id, name=project.name, description=project.description, status=project.status) for project in projects]
                  }
        
        
        return result