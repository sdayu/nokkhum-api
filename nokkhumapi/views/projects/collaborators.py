'''
Created on Jan 21, 2013

@author: boatkrap
'''
from pyramid.view import view_defaults
from pyramid.view import view_config

from nokkhumapi import models

@view_defaults(route_name='projects.collaborators', renderer="json", permission="authenticated")
class ProjectCollaborator:
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get_collaborators(self):
        matchdict = self.request.matchdict
        project_id = matchdict['project_id']
        
        project = models.Project.objects(project_id).first()
        if project is None:
            self.request.response.status = '404 Not Found'
            return {'message':"Project id %d not found"%project_id}
        
        result = dict(
                      project=dict(id=project.id, name=project.name, collaborators=[]),
                      )
        
        for collaborator in project.collaborators:
            
            result['project']['collaborators'].append(
                dict(
                     id=collaborator.user.id,
                     email=collaborator.user.email
                     )    
                )
        self.request.response.headers['Access-Control-Allow-Origin'] = '*'
        return result
    
    @view_config(request_method='POST')
    def add(self):
        matchdict = self.request.matchdict
        project_id = matchdict['project_id']
        collaborator_dict = self.request.json_body['collaborator']
        
        user = models.User.objects(id=collaborator_dict['id']).first()
        project = models.Project.objects(id=project_id).first()
        
        
        if user is None or project is None:
            self.request.response.status = '500 Internal Server Error'
            return {'message':"Project or user not found"}
        
        for collaborator in project.collaborators:
            if collaborator.user == user:
                self.request.response.status = '500 Internal Server Error'
                return {'message':"This user is project collaborator"}
        
        collaborator = models.Collaborator()
        collaborator.user = user
        
        project.collaborators.append(collaborator)
        
        project.save()
        self.request.response.headers['Access-Control-Allow-Origin'] = '*'
        return collaborator_dict
    
    @view_config(request_method='PUT')
    def update_collaborator(self):
        pass
    
    @view_config(request_method='DELETE')
    def delete(self):
        matchdict = self.request.matchdict
        project_id = matchdict['project_id']
        
        collaborator_dict = self.request.json_body['collaborator']
        
        user = models.User.objects(id=collaborator_dict['id']).first()
        project = models.Project.objects(id=project_id).first()
        
        if user is None or project is None:
            self.request.response.status = '500 Internal Server Error'
            return {'message':"Project or user not found"}
        
        for collaborator in project.collaborators:
            if collaborator.user == user:
                break
        
        project.collaborators.remove(collaborator)
        project.save()
        
        return collaborator_dict