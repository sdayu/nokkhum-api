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
        pp=pprint.PrettyPrinter(indent=4)
        #login
        args = dict(password_credentials= {"email": "admin@nokkhum.local", 
                                          "password": "password"}
                    )
        response = self.testapp.post_json('/authentication/tokens', params=args, status=200)
        print("authentication: ")
        self.pp.pprint(response.json)
        
        token = response.json['access']['token']['id']
        
        response = self.testapp.get('/operating/{camera_id}/camera', headers=[('X-Auth-Token', token)], status=200)
        print("responce get :")
        pp.pprint(response.json)
        
        
       
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    
    