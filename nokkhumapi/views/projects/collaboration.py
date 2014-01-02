'''
Created on Jan 1, 2014
@author: yoschanin.s
'''
from pyramid.view import view_defaults
from pyramid.view import view_config

from nokkhumapi import models

@view_defaults(route_name='projects.collaboration', renderer="json", permission="authenticated")
class ProjectCollaborator:
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get_collaborators(self):
        pass
    
    @view_config(request_method='POST')
    def add(self):
        matchdict = self.request.matchdict
        project_id = matchdict['project_id']
        collaborator_dict = self.request.json_body['collaborator']
        
        if collaborator_dict['type'] == 'group' :
            data = models.Group.objects(name=collaborator_dict['name']).first()
        elif collaborator_dict['type'] == 'user' :
            data = models.User.objects(email=collaborator_dict['email']).first()
            
        project = models.Project.objects(id=project_id).first()
        
        if data is None or project is None:
            self.request.response.status = '500 Internal Server Error'
            return {'message':"Project or user not found"}
        
        if collaborator_dict['type'] == 'group' :
            for collaborator in project.gcollaborators:
                if collaborator == data:
                    self.request.response.status = '500 Internal Server Error'
                    return {'message':"This Group is project collaborator"}
            project.gcollaborators.append(data)
            for gcollaborator in project.gcollaborators:
                if gcollaborator == data:
                    for collaborator in gcollaborator.collaborators:
                        if collaborator.user == project.owner:
                            processors=models.Processor.objects(project=project)
                            for processor in processors:
                                gcollaborator = models.GroupCollboratorPermission()
                                gcollaborator.processor = processor
                                gcollaborator.permissions.append('view')
                                collaborator.camera_permissions.append(gcollaborator)
                            break
                    break
            
        elif collaborator_dict['type'] == 'user' :
            for collaborator in project.collaborators:
                if collaborator.user == data:
                    self.request.response.status = '500 Internal Server Error'
                    return {'message':"This user is project collaborator"}
            collaborator = models.Collaborator()
            collaborator.user = data
            project.collaborators.append(collaborator)
            processors=models.Processor.objects(project=project)
            for processor in processors:
                pcollaborator = models.CollboratorPermission()
                pcollaborator.processor = processor
                pcollaborator.permissions.append('view')
                collaborator.camera_permissions.append(pcollaborator)
        
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