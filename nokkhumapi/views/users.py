'''
Created on Jul 6, 2012

@author: coe
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from ..import models
@view_defaults(route_name='users', renderer="json")
class userView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        id = int(extension[0])
        
        user = models.User.objects(id=id).first()
        
        if not user:
            self.request.response.status = '404 Not Found'
            return {}
        result = {"user":{}}
        result["user"]["id"] = user.id
        result["user"]["email"] = user.email
        result["user"]["password"] = user.password
        result["user"]["first_name"] = user.first_name
        result["user"]["last_name"] = user.last_name
        result["user"]["status"] = user.status
        result["user"]["group"] = {"id": user.group.id, "name":user.group.name}
        
        return result
    
    @view_config(request_method='POST')
    def create(self):
        
        user_dict = self.request.json_body["user"]
        user            = models.User()
        user.first_name = user_dict["first_name"]
        user.last_name  = user_dict["last_name"]
        user.email      = user_dict["email"]
        user.password   = user_dict["password"]
        
        group           = models.Group.objects(name=user_dict["group"]["name"]).first()
        user.group      = group
        
        user.save()
        
        user_dict["id"] = user.id
        result = {"user":user_dict}
        
        
        return result
    
    @view_config(request_method='PUT')
    def update(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        id = int(extension[0])
        
        user = models.User.objects(id=id).first()
        
        if not user:
            self.request.response.status = '404 Not Found'
            return {'result':"not found id: %d"%id}
        
        user_dict = self.request.json_body["user"]
        user.first_name= user_dict["first_name"]
        user.last_name = user_dict["last_name"]
        user.email = user_dict["email"]
        user.password = user_dict["password"]
        user.save()
        
        result = {"user":user_dict}
        return result
        
    @view_config(request_method='DELETE')
    def delete(self):
        matchdict = self.request.matchdict
        extension = matchdict.get('extension')
        id = int(extension[0])
    
        user = models.User.objects(id=id).first()
        if not user:
            self.request.response.status = '404 Not Found'
            return {'result':"not found id: %d"%id}
    
        user.delete()

        return {'result':"delete success"}

                
        