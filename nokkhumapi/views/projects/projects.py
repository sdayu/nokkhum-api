'''
Created on Oct 22, 2012

@author: coe
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models
@view_defaults(route_name='projects', renderer="json", permission="authenticated")
class ProjectView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        project_id = extension[0]
        
        project = models.Project.objects(id=project_id).first()

        if not project:
            self.request.response.status = '404 Not Found'
            return {}
        
        result = dict(
                      project=dict(
                            id=project.id,
                            name=project.name,
                            description=project.description,
                            status=project.status,
                            created_date=project.created_date,
                            updated_date=project.updated_date,
                            ip_address=project.ip_address,
                            user=dict(
                                id=project.owner.id, 
                                username=project.owner.email),
                            colaborators=[dict(id=collaborator.user.id, email=collaborator.user.email) 
                                          for collaborator in project.collaborators],
                            gcolaborators=[dict(id=collaborator.id, name=collaborator.name) 
                                          for collaborator in project.gcollaborators]
                            )
                      
                      )

        return result
    
    @view_config(request_method='POST')   
    def create(self):
        project_dict = self.request.json_body["project"]

        project = models.Project()
        project.name = project_dict["name"]
        project.description = project_dict["description"]
        project.status = project_dict.get('status', 'active')
        project.created_date = datetime.datetime.now()
        project.updated_date = datetime.datetime.now()
        project.ip_address = self.request.environ.get('REMOTE_ADDR', '0.0.0.0')
        project.owner = self.request.user
        project.save() 
        
        project_dict["id"] = project.id
        return {"project":project_dict}
    @view_config(request_method='PUT')
    def update(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        id = int(extension[0])
        
        project = models.Project.objects(id=id).first()
        
        if not project:
            self.request.responce.status='404 Not Found'
            return {'result':"not found id : %d"%id}
        
        project_dict = self.request.json_body["project"]
        project.name = project_dict["name"]
        project.description = project_dict["description"]
        project.updated_date = datetime.datetime.now()
        
        if 'status' in project_dict:
            project.status = project_dict["status"]

        #project.owner = project_dict["owner"]
        project.save()
        
        result = {"project":project_dict}
        return result
    @view_config(request_method='DELETE')
    def delete(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        id = extension[0]
        
        project = models.Project.objects(id=id).first()
        if not project:
            self.request.responce.status = '404 Not Found'
            return {'result':"not found id : %d"%id}
        
        project.delete()
        
        return {'result':"Delete suscess"}
