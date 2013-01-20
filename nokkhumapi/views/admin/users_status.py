'''
Created on Jan 20, 2013

@author: wongpiti
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

USER_STATUS = ['active', 'disactive', 'delete']

@view_config(route_name='admin.users.users_status', renderer='json', permission="r:admin", request_method='GET')
def list_user_by_status(request):
    matchdict = request.matchdict
    status_name = matchdict['status_name']
    
    if status_name.lower() not in USER_STATUS:
        request.response.status = '500 Internal Server Error'
        return {'message':"status %s not define"%status_name}
        
    users = models.User.objects(status__iexact=status_name).all()
    
    
    return dict(
            users=[dict(id=user.id, email=user.email) for user in users]
            )

@view_config(route_name='admin.users.set_status', renderer='json', permission="r:admin", request_method='POST')
def set_user_status(request):
    matchdict = request.matchdict
    user_id = matchdict['user_id']
    status_name = matchdict['status_name']
    
    user = models.User.objects(id=user_id).first()
    if user is None:
        request.response.status = '404 Not Found'
        return {'result':"not found id: %d"%id}
    user.status = status_name
    user.save()
    
    return dict(
                user = dict(id=user.id, email=user.email, status=user.status)
                )
   
   
     
     