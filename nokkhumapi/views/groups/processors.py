'''
Created on Jan 21, 2013

@author: boatkrap
'''
from pyramid.view import view_defaults
from pyramid.view import view_config

from nokkhumapi import models

@view_defaults(route_name='groups.processors', renderer="json", permission="authenticated")
class GroupCollaborator:
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def gets(self):
        matchdict = self.request.matchdict
        group_id = matchdict['group_id']
        
        group = models.Group.objects(id=group_id).first()
        if group is None:
            self.request.response.status = '404 Not Found'
            return {'message':"Group id %d not found"%project_id}
        collaborate_projects = models.Project.objects().all()
        print(collaborate_projects)
        result = dict(
                      group=dict(id=group.id, name=group.name, collaborators=[]),
                      )
        
        for collaborator in group.collaborators:
            result['group']['collaborators'].append(
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
        group_id = matchdict['group_id']
        collaborator_dict = self.request.json_body['collaborator']
        
        user = models.User.objects(id=collaborator_dict['id']).first()
        group = models.Group.objects(id=group_id).first()
        
        if user is None or group is None:
            self.request.response.status = '500 Internal Server Error'
            return {'message':"Project or user not found"}
        
        for collaborator in group.collaborators:
            if collaborator.user == user:
                self.request.response.status = '500 Internal Server Error'
                return {'message':"This user is project collaborator"}
        
        collaborator = models.GroupCollaborator()
        collaborator.user = user
        collaborator.permissions.append('user')
        
        group.collaborators.append(collaborator)
        
        group.save()
        self.request.response.headers['Access-Control-Allow-Origin'] = '*'
        return collaborator_dict
    
    @view_config(request_method='PUT')
    def update_collaborator(self):
        print('hi')
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