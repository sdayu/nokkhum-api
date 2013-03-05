'''
Created on Jan 3, 2013

@author: ww
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='projects.cameras', renderer="json", permission="authenticated")
class ProjectCamerasView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        project_id = matchdict.get('project_id')
        
        project = models.Project.objects(id=project_id).first()
        
        cameras = models.Camera.objects(project=project).all() 

        result = dict(
                      cameras=[dict(id=camera.id, name=camera.name) for camera in cameras]
                    )
                      
        
        return result
    
@view_defaults(route_name='projects.acamera', renderer="json", permission="authenticated")
class ProjectCameraView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        project_id = matchdict.get('project_id')
        id = matchdict.get('camera_id')
        
        project = models.Project.objects(id=project_id).first()
        
        if id.isdigit():
            camera = models.Camera.objects(id=id, project=project, owner=self.request.user).first()
        else:
            camera = models.Camera.objects(name=id, project=project, owner=self.request.user).first()
            
        print("get camera: ", camera.name)

        result = dict(
                      camera=dict(
                                  id=camera.id,
                                  name=camera.name
                                  )
                    )
                      
        
        return result