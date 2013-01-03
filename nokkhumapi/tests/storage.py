'''
Created on Jan 3, 2013

@author: boatkrap
'''
import unittest
import json
import pprint

import configparser

class StorageTest(unittest.TestCase):


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
        self.pp = pprint.PrettyPrinter(indent=4)

    def tearDown(self):
        pass


    def test_list_file(self):
        response = self.testapp.get('/storage', headers=[('X-Auth-Token', self.token)], status=200)
        print("response list file: ")
        self.pp.pprint(response.json)
        
        response = self.testapp.get('/storage/1', headers=[('X-Auth-Token', self.token)], status=200)
        print("response list file: ")
        self.pp.pprint(response.json)
        
        response = self.testapp.get('/storage/1/20130103/video', headers=[('X-Auth-Token', self.token)], status=200)
        print("response list file: ")
        self.pp.pprint(response.json)
        self.assertIn("download", response.json["files"][0]['download'])
        
    def test_download_file(self):
        response = self.testapp.get('/storage/1/20130103/video', headers=[('X-Auth-Token', self.token)], status=200)
        url = response.json["files"][0]['download']
        print("download url: ", url)
        response = self.testapp.get(url, headers=[('X-Auth-Token', self.token)], status=200)
    
    
    def test_delete_file(self):
        response = self.testapp.get('/storage/1', headers=[('X-Auth-Token', self.token)], status=200)
        url = response.json["files"][0]['url']+"/video"
        response = self.testapp.get(url, headers=[('X-Auth-Token', self.token)], status=200)
        url = response.json["files"][0]['url']
        response = self.testapp.delete(url, headers=[('X-Auth-Token', self.token)], status=200)
        self.pp.pprint(response.json)
        #response = self.testapp.get(url, headers=[('X-Auth-Token', self.token)], status=200)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()