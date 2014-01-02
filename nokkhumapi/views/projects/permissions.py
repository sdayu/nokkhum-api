'''
Created on Jan 2, 2014
@author: yoschanin.s
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='projects.permissions', renderer="json", permission="authenticated")
class ProjectProcessorView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        project_id = matchdict.get('project_id')
        user_id = matchdict.get('user_id')
        project = models.Project.objects(id=project_id).first()
        processors = models.Processor.objects(project=project, status='active').order_by("+name").all()
        user = models.User.objects(id=user_id).first()
        permission = []
        if user is None:
            user = models.Group.objects(id=user_id).first()
            for group in project.gcollaborators:
                if group == user:
                    for collaborator in group.collaborators:
                        if collaborator.user == project.owner:
                            for camera_permission in collaborator.camera_permissions:
                                for processor in processors:
                                    if camera_permission.processor == processor:
                                        permission.append(dict(id=processor.id, name=processor.name,permissions=camera_permission.permissions))
                                        break
                            break
                    break
        else:
            for collaborator in project.collaborators:
                if collaborator.user == user:
                    for camera_permission in collaborator.camera_permissions:
                        for processor in processors:
                            if camera_permission.processor == processor:
                                permission.append(dict(id=processor.id, name=processor.name,permissions=camera_permission.permissions))
                                break
                    break
                
        result = dict(
                      permissions=permission
                    )
                      
        return result
    
    @view_config(request_method='POST')
    def post(self):
        matchdict = self.request.matchdict
        project_id = matchdict.get('project_id')
        
        project = models.Project.objects(id=project_id).first()
        
        processors = models.Processor.objects(project=project, status='active').order_by("+name").all() 

        result = dict(
                      processors=[dict(id=processor.id, name=processor.name) for processor in processors]
                    )
                      
        return result
    
    @view_config(request_method='PUT')
    def update(self):
        matchdict = self.request.matchdict
        print(matchdict)
        project_id = matchdict.get('project_id')
        user_id = matchdict.get('user_id')
        permissions = self.request.json_body["permissions"]
        
        project = models.Project.objects(id=project_id).first()
        user = models.User.objects(id=user_id).first()
        
        if user is None:
            user = models.Group.objects(id=user_id).first()
            for group in project.gcollaborators:
                if group == user:
                    for collaborator in group.collaborators:
                        if collaborator.user == project.owner:
                            for camera_permission in collaborator.camera_permissions:
                                for permission in permissions:
                                    if camera_permission.processor == processor:
                                        
                                        break
                            break
                    break
        else:
            for collaborator in project.collaborators:
                if collaborator.user == user:
                    for camera_permission in collaborator.camera_permissions:
                        for permission in permissions:
                            if camera_permission.processor.id == permission['id']:
                                if permission['permission'] == 'noview':
                                    camera_permission.permissions.remove('view')
                                elif (permission['permission'] == 'view') and not(permission['permission'] in camera_permission.permissions):
                                    camera_permission.permissions.append('view')
                                elif permission['permission'] == 'nostroage':
                                    camera_permission.permissions.remove('stroage')
                                elif (permission['permission'] == 'stroage') and not (permission['permission'] in camera_permission.permissions):
                                    camera_permission.permissions.append('stroage')
                                break
                    break
        project.save()          
        return {'permissions': {}}
