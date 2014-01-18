'''
Created on Dec 28, 2013

@author: yoschanin.s
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='groups.usergroups', renderer="json", permission="authenticated")
class UserGroupsView(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        user_id = matchdict.get('user_id')
        user = models.User.objects(id=user_id).first()
        
        if not user:
            self.request.response.status = '404 Not Found'
            return {'error':{'message':'This user not found.'}}
        
        collaborate_groups = models.Group.objects(collaborators__user=user).all()

        result = {
                  "collaborate_groups":[dict(id=group.id, 
                                   name=group.name, 
                                   description=group.description,
                                   create_date=group.create_date
                                   )
                               for group in collaborate_groups]
                  }
        
        return result