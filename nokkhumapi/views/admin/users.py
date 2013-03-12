'''
Created on 12 Jan 2013

@author: ww
'''

from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='admin.users', renderer="json", permission="authenticated")
class User:
    def __init__(self, request):
        self.request = request
        
    @view_config(route_name='admin.users.list', renderer="json", permission="authenticated", request_method='GET')
    def list_user(self):
        
        results = []
        users=models.User.objects().all()
        
        for user in users:
            results.append({'id':user.id, 'email':user.email})
        
        return dict(
                users=[dict(
                            id=user.id, 
                            email=user.email,
                            first_name=user.first_name,
                            last_name=user.last_name,
                            status=user.status,
                            registration_date=user.registration_date,
                            update_date=user.update_date,
                            roles=[dict(
                                        id=role.id,
                                        name=role.name
                                        )
                                    for role in user.roles
                                   ]
                            )
                       for user in users]
                )
            
            
    @view_config(request_method='GET')
    def show_user(self):
        matchdict = self.request.matchdict
        user_id = matchdict['user_id']
        user = models.User.objects().with_id(user_id)
        
        result = dict(user=dict(
                            id=user.id,
                            email=user.email,
                            password=user.password,
                            first_name=user.first_name,
                            last_name=user.last_name,
                            status=user.status,
                            registration_date=user.registration_date,
                            update_date=user.update_date,
                            roles=[dict(
                                        id=role.id,
                                        name=role.name
                                        )
                                    for role in user.roles
                                   ]
                            )
                      )
        return result
    
    
    
