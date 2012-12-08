'''
Created on Dec 6, 2012

@author: coe
'''
from pyramid.view import  view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from .. import models

@view_defaults(route_name='accounts', renderer="json")
class AccountView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='POST')
    def register(self):
        user_dict = self.request.json_body["user"]
        
        
        if len(user_dict["email"]) == 0 or len(user_dict["password"]) == 0:
            self.request.response.status = '500 Internal Server Error'
            return {'error':{'message':'Required email and password.'}}
        
        user = models.User.objects(email=user_dict["email"]).first()
        if user:
            self.request.response.status = '500 Internal Server Error'
            return {'error':{'message':'This email is available on system.'}}
        
        
        user            = models.User()
        user.first_name = user_dict["first_name"]
        user.last_name  = user_dict["last_name"]
        user.email      = user_dict["email"]
        user.password   = self.request.secret_manager.get_hash_password(user_dict["password"])
        
        role           = models.Role.objects(name='user').first()
        user.roles.append(role)
        
        user.save()
        
        user_dict["id"] = user.id
        result = {"user":user_dict}
        
        
        return result

