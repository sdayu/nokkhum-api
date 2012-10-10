'''
Created on Oct 10, 2012

@author: boatkrap
'''
import unittest
from pyramid import testing
from pyramid.config import Configurator

class CameraApiTest(unittest.TestCase):

    def setUp(self):
        from .. import main
        settings = {'mongodb.db_name': 'nokkhum', 'mongodb.host': 'localhost'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_root(self):
        response = self.testapp.get('/cameras/1', status=200)
        print (response.body)
#        self.failUnless('Pyramid' in res.body)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()