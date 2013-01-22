'''
Created on Jan 18, 2013

@author: boatkrap
'''
import urllib.parse
class CameraDriver:
    def __init__(self, host, username, password, port=80):
        self.host = host
        self.username = username
        self.password = password
        
        self.protocal = 'http'
        self.port = port
        
        self.auth = ''
        self.add_port = ''
        self.__process()
        
    def __process(self):
        if len(self.username) > 0:
            self.auth = "{username}:{password}@".format(username=urllib.parse.quote(self.username), password=urllib.parse.quote(self.password))
            
        if self.port != 80:
            self.add_port=':{}'.format(self.port)
        
    def get_base_url(self):
        
        self.__process()
        return "{protocal}://{auth}{host}{add_port}"\
            .format(**self.__dict__)