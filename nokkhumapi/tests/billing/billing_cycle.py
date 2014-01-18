'''
Created on Nov 27, 2013

@author: wongpiti
'''

import unittest
import configparser, pprint
import datetime

class Test(unittest.TestCase):
    def setUp(self):
        from nokkhumapi import main
        
        cfg = configparser.ConfigParser()
        cfg.read('../../../development.ini')
        
        settings = dict(cfg.items('app:main'))

        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

        args = dict(password_credentials= {"username": "admin@nokkhum.local", 
                                          "password": "password"}
                    )
        response = self.testapp.post_json('/authentication/tokens', params=args, status=200)
        print("authentication: ")
        
        self.pp=pprint.PrettyPrinter(indent=4)
        self.pp.pprint(response.json)
        
        self.token = response.json['access']['token']['id']
        self.user = response.json['access']['user']

    def tearDown(self):
        pass
    
    def test_calculate_bill(self):
        response_projects = self.testapp.get('/users/%s/projects'%self.user['id'], headers=[('X-Auth-Token', self.token)], status=200)
        current_project = response_projects.json['projects'][0]
                                   

        response_processors = self.testapp.get('/projects/%s/processors'%current_project['id'], headers=[('X-Auth-Token', self.token)], status=200)
        
        processor_id = response_processors.json['processors'][0]['id']
        print("processor_id", processor_id)
        response = self.testapp.get('/billing/processors/%s/cycle'%processor_id,
                                    headers=[('X-Auth-Token', self.token)], status=200)
        self.pp.pprint(response.json)  
            
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
        
        
        
        
        
        
        