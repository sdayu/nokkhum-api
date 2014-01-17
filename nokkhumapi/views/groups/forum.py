'''
Created on Jan 16, 2014

@author: yoschanin.s
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response
import re
import json, datetime

from nokkhumapi import models
@view_defaults(route_name='forums', renderer="json", permission="authenticated")
class ForumView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        group_id = extension[0]
        print('>>', group_id)
#         if not re.search('\d+', group_id):
#             # no numbers
#             group = models.Group.objects(name=group_id, collaborators__user=self.request.user).first()
#         else:
#             # numbers present
#             group = models.Group.objects(id=group_id, collaborators__user=self.request.user).first()
#         if not group:
#             self.request.response.status = '404 Not Found'
#             return {}
#         
#         result = dict(
#                       group=dict(
#                             id=group.id,
#                             name=group.name,
#                             description=group.description,
#                             status=group.status,
#                             create_date=group.create_date,
#                             update_date=group.update_date,
#                             ip_address=group.ip_address,
#                             colaborators=[dict(id=collaborator.user.id, email=collaborator.user.email, permissions=[permission for permission in collaborator.permissions]) 
#                                           for collaborator in group.collaborators],
#                             )
#                       
#                       )
        result = dict(
                      forums=dict()
                      )
        return result
    
    @view_config(request_method='POST')   
    def create(self):
        topic = self.request.json_body["topic"]

        forum = models.Forum()
        forum.description = topic["description"]
        forum.create_date = datetime.datetime.now()
        forum.update_date = datetime.datetime.now()
        forum.ip_address = self.request.environ.get('REMOTE_ADDR', '0.0.0.0')
        
        forum.owner = self.request.user
        group = models.Group.objects(id=topic["group_id"],collaborators__user=self.request.user).first()        
        if group is None:
            self.request.response.status = '404 Not Found'
            return {}
        
        forum.group = group
        forum.save()
        
        return {}
    
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