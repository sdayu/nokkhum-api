'''
Created on Jan 18, 2013

@author: boatkrap
'''

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
            self.auth = "{username}:{password}@".format(**self.__dict__)
            
        if self.port != 80:
            self.add_port=':{}'.format(self.port)
        
    def get_base_url(self):
        
        self.__process()
        return "{protocal}://{auth}{host}{add_port}"\
            .format(**self.__dict__)