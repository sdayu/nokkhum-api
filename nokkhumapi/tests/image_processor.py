'''
Created on Dec 30, 2012

@author: ww
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
        self.pp = pprint.PrettyPrinter(indent=4)
        

    def test_image_processor(self):
        
        args=[
              {
                "width": 640,
                "maximum_wait_motion": 5,
                "name": "Video Recorder",
                "fps": 10,
                "record_motion": True,
                "height": 480
                }
            ]
        
        print("args: ", args)
        response = self.testapp.post_json('/camera/1/processors', params={'processors':args}, headers=[('X-Auth-Token', self.token)], status=200)
        print("responce post :")
        self.pp.pprint(response.json)
        
        
       
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()