'''
Created on Jan 31, 2013

@author: wongpiti
'''
import unittest
import pprint
import configparser

class TestUserList(unittest.TestCase):

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
        
        self.user_id = 1
        
        
    def test_list_user(self):
        response = self.testapp.get('/co_users/users', headers=[('X-Auth-Token', self.token)], status=200)
        print( "response get: ")
        self.pp.pprint(response.json)
        
    def test_show_user(self):
        response = self.testapp.get('/co_users/users/%d'%self.user_id, headers=[('X-Auth-Token', self.token)], status=200)
        print( "response get: ")
        self.pp.pprint(response.json)         
       
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()