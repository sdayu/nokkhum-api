'''
Created on Dec 26, 2012

@author: ww
'''
import unittest
import pprint
import configparser

class TestSelectProject(unittest.TestCase):

    def setUp(self):
        from nokkhumapi import main
        
        cfg = configparser.ConfigParser()
        cfg.read('../../development.ini')
        
        settings = dict(cfg.items('app:main'))

        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

        args = dict(password_credentials= {"email": "admin@nokkhum.local", 
                                          "password": "password"}
                    )
        response = self.testapp.post_json('/authentication/tokens', params=args, status=200)
        print("authentication: ")
        
        self.pp=pprint.PrettyPrinter(indent=4)
        self.pp.pprint(response.json)
        
        self.token = response.json['access']['token']['id']
        
        self.camera_id = 1
        
    def test_operation(self):

        
        args={'camera_operating':{
                           'action':'start'
                           }
              
              }
        response = self.testapp.post_json('/cameras/%d/operating'%self.camera_id, params=args, headers=[('X-Auth-Token', self.token)], status=200)
        print("responce post :")
        self.pp.pprint(response.json)
        
        response = self.testapp.get('/cameras/%d/operating'%self.camera_id, headers=[('X-Auth-Token', self.token)], status=200)
        print( "response get: ")
        self.pp.pprint(response.json)
        
            
       
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    
    