'''
Created on 12 Jan 2013

@author: ww
'''

from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_config(route_name='admin.users.list_users', renderer="json", permission="authenticated", request_method='GET')
def list_user(request):
    
    results = []
    users=models.User.objects().all()
    
    for user in users:
        results.append({'id':user.id, 'email':user.email})
    request.response.headers['Access-Control-Allow-Origin'] = '*'
    return dict(
            users=results
            )
        
        
@view_config(route_name='admin.users.show_users', renderer="json", permission="authenticated", request_method='GET')
def show_user(request):
    matchdict = request.matchdict
    user_id = matchdict['user_id']
    user = models.User.objects().with_id(user_id)
    
    result = {"user":{}}
    result["user"]["id"]=user.id
    result["user"]["email"]=user.email
    result["user"]["password"]=user.password
    result["user"]["first_name"]=user.first_name
    result["user"]["last_name"]=user.last_name
    result["user"]["status"]=user.status
    request.response.headers['Access-Control-Allow-Origin'] = '*'
    return result



