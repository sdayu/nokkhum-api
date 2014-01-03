'''
Created on Dec 8, 2012

@author: wongpiti
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='projects.userprojects', renderer="json", permission="authenticated")
class UserProjectsView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        user_id = matchdict.get('user_id')
        
        user = models.User.objects(id=user_id).first()
        if not user:
            self.request.response.status = '404 Not Found'
            return {'error':{'message':'This user not found.'}}
        
        projects = models.Project.objects(owner=user).order_by("+name").all()
        collaborate_projects = models.Project.objects(collaborators__user=user).all()

        result = {
                  "projects":[dict(id=project.id, 
                                   name=project.name, 
                                   description=project.description, 
                                   camera_number=project.get_camera_number(),
                                   processor_number=project.get_processor_number(),
                                   create_date=project.create_date
                                   )
                               for project in projects],
                  "collaborate_projects":[dict(id=project.id, name=project.name, description=project.description, owner=project.owner.email, ownerid=project.owner.id) for project in collaborate_projects]
                  }
        
        return result