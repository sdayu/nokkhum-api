'''
Created on Oct 22, 2012

@author: coe
'''
import unittest
import pprint
import configparser

class ProjectGetCollaborator(unittest.TestCase):


    def setUp(self):
        from nokkhumapi import main
        
        cfg = configparser.ConfigParser()
        cfg.read('../../../development.ini')
        
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
        
        self.project_id = 1

    def tearDown(self):
        pass

    def test_project_get_collaborate(self):

        response = self.testapp.get('/projects/%d'%self.project_id, headers=[('X-Auth-Token', self.token)], status = 200)
        print("response get")
        self.pp.pprint(response.json)
        
        self.assertEqual(response.json["project"]["id"], self.project_id)
        self.project_dict =  response.json["project"]
        
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()