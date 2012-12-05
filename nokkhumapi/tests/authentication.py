'''
Created on Oct 10, 2012

@author: boatkrap
'''
import unittest
from pyramid import testing
from pyramid.config import Configurator

import json
import pprint

class AuthenticationApiTest(unittest.TestCase):

    def setUp(self):
        from .. import main
        
        settings = {'mongodb.db_name': 'nokkhum',
                    'mongodb.host': 'localhost',
                    'nokkhum.auth.secret': 'nokkhum'}
        
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
        
        self.pp = pprint.PrettyPrinter(indent=4)
    
    def test_authentication(self):
        
        # create camera
        args = dict(password_credentials= {"email": "admin@nokkhum.local", 
                                          "password": "password"}
                    )
        response = self.testapp.post_json('/authentication/tokens', params=args, status=200)
        print("authentication: ")
        self.pp.pprint(response.json)
        import time
        time.sleep(5)
        
        response = self.testapp.get('/authentication/tokens', headers={'X-Auth-Token':response.json['access']['token']['id']}, status=200)
        #response = self.testapp.get('/authentication/tokens', headers={'X-Auth-Token':'test'}, status=200)
        print("test_get: ")
        self.pp.pprint(response.json)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    unittest.main()