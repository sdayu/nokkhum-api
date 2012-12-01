'''
Created on Oct 22, 2012

@author: coe
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from ..import models
@view_defaults(route_name='projects', renderer="json")
class ProjectView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        id = int(extension[0])
        
        project = models.Project.objects(id=id).first()
        
        if not project:
            self.request.response.status = '404 Not Found'
            return {}
        result = {"project":{}}
        result["project"]["id"] = project.id
        result["project"]["name"] = project.name
        result["project"]["description"] = project.description
        result["project"]["status"] = project.status
        result["project"]["create_date"] = project.create_date
        result["project"]["update_date"] = project.update_date
        result["project"]["ip_address"] = project.ip_address
        result["project"]["user"] = dict(id=project.owner.id, username=project.owner.email)
        
        return result
    
    @view_config(request_method='POST')   
    def create(self):
        project_dict = self.request.json_body["project"]
        print("project dict: ", project_dict)
        print("environ: ", self.request.environ)
        
        user_dict = self.request.json_body["project"]["user"]
        
        project = models.Project()
        
        project.name = project_dict["name"]
        project.description = project_dict["description"]
        project.status = project_dict.get('status', 'Active')
        project.create_date = datetime.datetime.now()
        project.update_date = datetime.datetime.now()
        project.ip_address = self.request.environ.get('REMOTE_ADDR', '0.0.0.0')
        project.owner = models.User.objects(id=user_dict["id"]).first()
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
        project.descriptio = project_dict["description"]
        project.status = project_dict["status"]

        #project.owner = project_dict["owner"]
        project.save()
        
        result = {"project":project_dict}
        return result
    @view_config(request_method='DELETE')
    def delete(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        id = int(extension[0])
        
        project = models.Project.objects(id=id).first()
        if not project:
            self.request.responce.status = '404 Not Found'
            return {'result':"not found id : %d"%id}
        
        project.delete()
        
        return {'result':"Delete suscess"}
