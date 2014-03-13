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
        group = models.Group.objects(id=group_id, collaborators__user=self.request.user).first()
        
        if group is None:
            self.request.response.status = '404 Not Found'
            return {'result':"not found id : %d"%group_id}
        
        forums = models.Forum.objects(group=group).all()
        
        result = dict(
                      forums=[dict(id=forum.id,
                                   description=forum.description,
                                   ownerid=forum.owner.id,
                                   name=forum.owner.email,
                                   created_date=forum.created_date,
                                   replys=[dict(description=reply.description, name=reply.user.email)for reply in forum.replys]) 
                                   for forum in forums]
                      )
        return result
    
    @view_config(request_method='POST')   
    def create(self):
        topic = self.request.json_body["topic"]
        if topic["forum_id"] is '':
            forum = models.Forum()
            forum.description = topic["description"]
            forum.created_date = datetime.datetime.now()
            forum.updated_date = datetime.datetime.now()
            forum.ip_address = self.request.environ.get('REMOTE_ADDR', '0.0.0.0')
            
            forum.owner = self.request.user
            group = models.Group.objects(id=topic["group_id"],collaborators__user=self.request.user).first()        
            if group is None:
                self.request.response.status = '404 Not Found'
                return {}
            
            forum.group = group
            forum.save()
        else: 
            forum = models.Forum.objects(id=topic["forum_id"]).first() 
            if forum is None:
                self.request.response.status = '404 Not Found'
                return {}
            reply = models.Reply()
            reply.description = topic["description"]
            reply.user = self.request.user
            
            forum.replys.append(reply)
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