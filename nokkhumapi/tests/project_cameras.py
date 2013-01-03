'''
Created on Dec 24, 2012

@author: ww unsure
'''

import unittest
import pprint

import configparser

class TestSelectProject(unittest.TestCase):

    def setUp(self):
        from .. import main
        
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
        self.user_id = response.json['access']['user']['id']
        self.pp = pprint.PrettyPrinter(indent=4)

    
    def test_select_project(self):
        response = self.testapp.get('/users/%d/projects'%self.user_id,  headers=[('X-Auth-Token', self.token)], status = 200)
        self.pp.pprint(response.json)
        
        project_id = response.json['projects'][0]['id']
        
        response = self.testapp.get('/projects/%d/cameras'%project_id,  headers=[('X-Auth-Token', self.token)], status = 200)
        print("response get")
        self.pp.pprint(response.json)
        
        
       
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()