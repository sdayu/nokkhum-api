'''
Created on Jan 21, 2013

@author: boatkrap
'''
import unittest
import configparser, pprint


class ProjectCollaboratorTest(unittest.TestCase):


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


    def test_collaborator(self):
        args = dict(
            collaborator=dict(
                      id=2
                      )
            )
        response = self.testapp.post_json('/projects/%d/collaborators'%self.project_id, params=args, headers=[('X-Auth-Token', self.token)], status=200)
        print('post response:')
        self.pp.pprint(response.json)
        
        response = self.testapp.get('/projects/%d/collaborators'%self.project_id, params=args, headers=[('X-Auth-Token', self.token)], status=200)
        print('get response:')
        self.pp.pprint(response.json)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()