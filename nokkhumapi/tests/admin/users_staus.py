'''
Created on Jan 20, 2013

@author: wongpiti
'''
import unittest
import pprint
import configparser

class TestUserList(unittest.TestCase):

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
        
        self.status_name = 'active'
        self.user_id = 1
    def test_list_user_by_status(self):
        response = self.testapp.get('/admin/users/status/%s'%self.status_name, headers=[('X-Auth-Token', self.token)], status=200)
        print( "response list_user_by_status: ")
        self.pp.pprint(response.json)         
       
    def test_set_user_status(self):
        response = self.testapp.post_json('/admin/users/%d/status/%s'%(self.user_id, self.status_name), headers=[('X-Auth-Token', self.token)], status=200)
        print( "response set_user_status: ")
        self.pp.pprint(response.json)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()