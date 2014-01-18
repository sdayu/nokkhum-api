'''
Created on Dec 4, 2012

@author: boatkrap
'''

from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import remember

import json, datetime

from .. import models

import uuid

@view_defaults(route_name='authentications.tokens', renderer="json")
class Tokens(object):
    def __init__(self, request):
        self.request = request

    @view_config(request_method='POST')
    def tokens(self):

        password_credential = self.request.json_body['password_credentials']
        
        pass_hash = self.request.secret_manager.get_hash_password(password_credential['password'])
        user = models.User.objects(email=password_credential['username'],
                                   password=pass_hash,
                                   status='active')\
                                   .first()
        
        if user is None:
            self.request.response.status = '401 Unauthorized'
            return dict(message='username or password mismatch')
        
        now = datetime.datetime.now()
        
        ip_address = self.request.environ.get('REMOTE_ADDR', '0.0.0.0')
        token = models.Token.objects(user=user, ip_address=ip_address, expired_date__gt=now).first()
        
        if token is None:
            token = models.Token()
            token.user = user
            token.access_date   = now
            token.expired_date  = now + datetime.timedelta(hours=2)
            token.ip_address    = ip_address
            
            token.save()
        
        #headers = remember(self.request, user.email)
        #print("test Header: ",headers)
        if user.face_id is None:
            user.face_id = str(models.User.objects(face_id=None).count())
            user.save()
        
        result = {
            "access": {
                "token": {
                    "expire": token.expired_date, 
                    "id": str(token.id)
                }, 
                "user": {
                    "id": user.id, 
                    "first_name": user.first_name, 
                    "last_name": user.last_name,
                    "roles": [dict(id=role.id, name=role.name) for role in user.roles], 
                    "email": user.email,
                    "face_id" : user.face_id
                }
            }
        }
        
        return result

    @view_config(request_method='GET', permission="authenticated")
    def get_token(self):
        token = models.Token.objects(user=self.request.user).first()
        if not token:
            self.request.response.status = '401 Unauthorized'
            return {}
        
        user = self.request.user
        return {
            "access": {
                "token": {
                    "expire": token.expired_date, 
                    "id": str(token.id)
                }, 
                "user": {
                    "id": user.id, 
                    "name": user.first_name, 
                    "roles": [dict(id=role.id, name=role.name) for role in user.roles], 
                    "email": user.email,
                }
            }
        }