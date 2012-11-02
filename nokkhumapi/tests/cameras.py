'''
Created on Oct 10, 2012

@author: boatkrap
'''
import unittest
from pyramid import testing
from pyramid.config import Configurator

import json

class CameraApiTest(unittest.TestCase):

    def setUp(self):
        from .. import main
        settings = {'mongodb.db_name': 'nokkhum', 'mongodb.host': 'localhost'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
    
    def test_cameraview_can_push_data_to_database(self):
        
        # create camera
        args = dict(username='', password='', name='Boatty', url='', image_size='', fps=5, 
                    storage_periods=1
)
        response = self.testapp.post_json('/cameras', params={'camera':args}, status=200)
        print("response create: ", response.json)
        
        self.assertIn("id", response.json["camera"])

        self.camera_id = response.json["camera"]["id"]

        # retrieve camera via camera id
        response = self.testapp.get('/cameras/%d'%self.camera_id, status=200)
        print ("response get: ", response.json)
        
        self.assertEqual(response.json["camera"]["id"], self.camera_id)
        self.camera_dict =  response.json["camera"]
        
        # try to change name
        args = self.camera_dict
        args["name"] = '123'
        response = self.testapp.put_json('/cameras/1', params={'camera':args}, status=200)
        print("response update: ", response.json)
        
        self.assertIn("id", response.json["camera"])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    unittest.main()