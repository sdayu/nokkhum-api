'''
Created on Oct 10, 2012

@author: boatkrap
'''
import unittest
from pyramid import testing
from pyramid.config import Configurator

import json

class UserApiTest(unittest.TestCase):

    def setUp(self):
        from .. import main
        settings = {'mongodb.db_name': 'nokkhum', 'mongodb.host': 'localhost'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
    
    def test_userview_can_push_data_to_database(self):
        
        # create camera
        args = dict(email       = 'test@test.com', 
                    password    = '', 
                    first_name  = 'Boatty', 
                    last_name   = '', 
                    status      = 'Active',
                    group       = dict(name="user") 
                    )
        response = self.testapp.post_json('/users', params={'user':args}, status=200)
        print("response create: ", response.json)
        
        self.assertIn("id", response.json["user"])

        self.user_id = response.json["user"]["id"]

        # retrieve camera via camera id
        response = self.testapp.get('/users/%d'%self.user_id, status=200)
        print ("response get: ", response.json)
        
        self.assertEqual(response.json["user"]["id"], self.user_id)
        self.user_dict =  response.json["user"]
        
        # try to change name
        self.user_dict['status'] = 'Delete'
        args = self.user_dict
        
        response = self.testapp.put_json('/users/%d'%response.json["user"]["id"], params={'user':args}, status=200)
        print("response update: ", response.json)
        
        self.assertIn("id", response.json["user"])
        
        response = self.testapp.delete('/users/%d'%response.json["user"]["id"], status=200)
        print("response delete: ", response.json)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    unittest.main()