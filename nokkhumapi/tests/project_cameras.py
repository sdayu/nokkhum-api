'''
Created on Dec 24, 2012

@author: ww unsure
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
    
    
    def test_select_project(self):
        pp=pprint.PrettyPrinter(indent=4)
        #create project
        args = dict(password_credentials= {"email": "admin@nokkhum.local", 
                                          "password": "password"}
                    )
        response = self.testapp.post_json('/authentication/tokens', params=args, status=200)
        print("authentication: ")
        self.pp.pprint(response.json)
        
        token = response.json['access']['token']['id']
        
        args=dict(
                  name = 'xxx',
                  description="",
                  camera = {"id":1}
                  
                )
        response = self.testapp.post_json('/projects', params={'project':args},  headers=[('X-Auth-Token', token)], status=200)
        print("responce get :")
        pp.pprint(response.json)
        
        self.assertIn("id",response.json["project"])
        
        self.project_id = response.json["project"]["id"]
        
        #retrieve project via project id
        response = self.testapp.get('/projects/%d'%self.project_id,  headers=[('X-Auth-Token', token)], status = 200)
        print("response get")
        pp.pprint(response.json)
        
        self.assertEqual(response.json["project"]["id"], self.project_id)
        self.project_dict =  response.json["project"]
        
        #get projects from user id
        response = self.testapp.get('/cameras/1/projects',  headers=[('X-Auth-Token', token)], status = 200)
        print("response get")
        pp.pprint(response.json)
        
        
       
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()