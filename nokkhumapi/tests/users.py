'''
Created on Oct 10, 2012

@author: boatkrap
'''
import unittest
from pyramid import testing
from pyramid.config import Configurator

import json
import pprint
import configparser

class UserApiTest(unittest.TestCase):

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
    
    def test_userview_can_push_data_to_database(self):

        # create camera
        args = dict(email       = 'test@nokkhum.local', 
                    password    = '', 
                    first_name  = 'iErk', 
                    last_name   = 'HamHam', 
                    )
        response = self.testapp.post_json('/users', params={'user':args}, headers=[('X-Auth-Token', self.token)], status=200)
        print("response create: ")
        self.pp.pprint(response.json)
        
        self.assertIn("id", response.json["user"])

        self.user_id = 2

        # retrieve camera via camera id
        response = self.testapp.get('/users/%d'%self.user_id, headers=[('X-Auth-Token', self.token)], status=200)
        print ("response get: ")
        self.pp.pprint(response.json)
        
        self.assertEqual(response.json["user"]["id"], self.user_id)
        self.user_dict =  response.json["user"]
        
        # try to change name
        self.user_dict['status'] = 'suspend'
        args = self.user_dict
        
        response = self.testapp.put_json('/users/%d'%response.json["user"]["id"], headers=[('X-Auth-Token', self.token)], params={'user':args}, status=200)
        print("response update: ")
        self.pp.pprint(response.json)
        
        self.assertIn("id", response.json["user"])
        
        response = self.testapp.delete('/users/%d'%response.json["user"]["id"], status=200)
        print("response delete: ")
        self.pp.pprint(response.json)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    unittest.main()