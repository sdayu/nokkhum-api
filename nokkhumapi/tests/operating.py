'''
Created on Dec 26, 2012

@author: ww
'''
import unittest
import pprint

class TestSelectProject(unittest.TestCase):

    def setUp(self):
        from nokkhumapi import main
        settings = {'mongodb.db_name': 'nokkhum', 
                    'mongodb.host': 'localhost',
                    'nokkhum.auth.secret': 'nokkhum'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        self.pp=pprint.PrettyPrinter(indent=4)
        
    def testName(self):
        
        pass
    def test_operation(self):

        #login
        args = dict(password_credentials= {"email": "admin@nokkhum.local", 
                                          "password": "password"}
                    )
        response = self.testapp.post_json('/authentication/tokens', params=args, status=200)
        print("authentication: ")
        self.pp.pprint(response.json)
        
        token = response.json['access']['token']['id']
        
        
        args={'camera_operating':{
                           'action':'start'
                           }
              
              }
        response = self.testapp.post_json('/cameras/1/operating', params=args, headers=[('X-Auth-Token', self.token)], status=200)
        print("responce post :")
        self.pp.pprint(response.json)
        
        response = self.testapp.get('/cameras/{camera_id}/operating'%self.camera_id, headers=[('X-Auth-Token', token)], status=200)
        print( "response get: ")
        self.pp.pprint(response.json)
        
            
       
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    
    