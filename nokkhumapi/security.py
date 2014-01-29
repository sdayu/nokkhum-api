from . import models

from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid

from pyramid.authentication import AuthTktCookieHelper
from pyramid.security import Everyone, Authenticated

import datetime

class TokenAuthenticationPolicy(object):

    def __init__(self):
        ''''''

    def remember(self, request, principal, **kw):
        return None

    def forget(self, request):
        return None

    def unauthenticated_userid(self, request):
        result = request.environ.get('HTTP_X_AUTH_TOKEN', None)
        # print("HTTP_X_AUTH_TOKEN: ", result)
        if result:
            token = models.Token.objects(id=result, expired_date__gt=datetime.datetime.now()).first()
            if token is None:
                return None
                
        else: 
            return None
        
        return result

    def authenticated_userid(self, request):
        if request.user:
            token = models.Token.objects(user=request.user, expired_date__gt=datetime.datetime.now()).first()
            # print("token.id: ", token.id)
            return token.id

    def effective_principals(self, request):
        principals = [Everyone]
        user = request.user
        if user:
            principals += [Authenticated, 'user:%s' % user.id]
            principals.extend((['role:%s'%role.name for role in user.roles]))
        return principals
    
class RequestWithUserAttribute(Request):
    @reify
    def user(self):
        # <your database connection, however you get it, the below line
        # is just an example>
        # dbconn = self.registry.settings['dbconn']
        tokenid = unauthenticated_userid(self)
        if tokenid is not None:
            # this should return None if the user doesn't exist
            # in the database
            # return dbconn['users'].query({'id':userid})
            try:
                token=models.Token.objects(id=tokenid, expired_date__gt=datetime.datetime.now()).first()
            except:
                return None
            
            if not token:
                return None
            
            return token.user
        
    @reify
    def secret_manager(self):
        from pyramid.threadlocal import get_current_registry
        settings = get_current_registry().settings
        
        return settings.secret_manager
        
        
    @reify
    def userid(self):
        return unauthenticated_userid(self)
    
    @reify
    def s3_client(self):

        from .cloud.storage import s3
        from pyramid.threadlocal import get_current_registry
        setting = get_current_registry().settings

        access_key_id = setting.get('nokkhum.s3.access_key_id')
        secret_access_key = setting.get('nokkhum.s3.secret_access_key')
        host = setting.get('nokkhum.s3.host') 
        port = int(setting.get('nokkhum.s3.port'))
        secure = False
        if setting.get('nokkhum.s3.secure_connection') in ['true', 'True']:
            secure = True
        s3_storage = s3.S3Client(access_key_id, secret_access_key, host, port, secure)
        
        return s3_storage

import hashlib
from Crypto.Cipher import AES

class SecretManager:
    def __init__(self, secret):
        self.password_secret = secret
        self.key = ''
        
        if len(self.password_secret)%32 != 0:
            if len(self.password_secret) > 32:
                self.key = self.passwordSecret[:32]
                
            elif len(self.password_secret) < 32:
                self.key = self.password_secret + (' '*(32-len(self.password_secret)))
            
        
        Initial16bytes='0123456789ABCDEF' 
        self.crypt = AES.new(self.key, \
                        AES.MODE_CBC, Initial16bytes) 

#    def setPasswordSecret(self, secret):
#        self.passwordSecret = secret
    
    def get_password_secret(self):
        return self.password_secret

        
    def get_hash_password(self, password):

        salt = hashlib.sha1(self.get_password_secret().encode('utf-8'))
        hashPass = hashlib.sha1(password.encode('utf-8'))
        
        hashPass.update((self.get_password_secret() + salt.hexdigest()).encode('utf-8'))
        return hashPass.hexdigest()
    
    def get_encrypt_password(self, text):

        cypher = self.crypt.encrypt(text) 
        return cypher 
    
    
    def get_decrypt_password(self, cypher):

        plain_text = self.crypt.decrypt(cypher) 
        return plain_text
