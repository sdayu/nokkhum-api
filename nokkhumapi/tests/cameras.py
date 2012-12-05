'''
Created on Oct 10, 2012

@author: boatkrap
'''
import unittest
from pyramid import testing
from pyramid.config import Configurator


import pprint
import json

class CameraApiTest(unittest.TestCase):

    def setUp(self):
        from .. import main
        settings = {'mongodb.db_name': 'nokkhum', 
                    'mongodb.host': 'localhost',
                    'nokkhum.auth.secret': 'nokkhum'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
    
    def test_cameraview_can_push_data_to_database(self):
        pp = pprint.PrettyPrinter(indent=4)
        
        # create camera
        args = dict(username='',
                     password='', 
                     name='Boatty',
                     url='', 
                     image_size='', 
                     fps=5, 
                    storage_periods=1
)
        response = self.testapp.post_json('/cameras', params={'camera':args}, status=200)
        print("response create: ")
        pp.pprint(response.json)
        
        self.assertIn("id", response.json["camera"])

        self.camera_id = response.json["camera"]["id"]

        # retrieve camera via camera id
        response = self.testapp.get('/cameras/%d'%self.camera_id, status=200)
        print( "response get: ")
        pp.pprint(response.json)
        
        self.assertEqual(response.json["camera"]["id"], self.camera_id)
        self.camera_dict =  response.json["camera"]
        
        # try to change name
        args = self.camera_dict
        args["name"] = '123'
        response = self.testapp.put_json('/cameras/1', params={'camera':args}, status=200)
        print("response update: ") 
        pp.pprint( response.json)
        
        self.assertIn("id", response.json["camera"])
        # try to Delete
        self.camera_dict['status'] = 'Delete'
        response = self.testapp.delete('/cameras/%d'%response.json["camera"]["id"], status=200)
        print("response delete: ")
        pp.pprint(response.json)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    unittest.main()