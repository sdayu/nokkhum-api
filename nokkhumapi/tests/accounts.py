'''
Created on Dec 6, 2012

@author: coe
'''
import unittest
from pyramid import testing
from pyramid.config import Configurator

import json
import pprint

class AccountApiTest(unittest.TestCase):
    
    def setUp(self):
        from .. import main
        settings = {'mongodb.db_name':'nokkhum',
                    'mongodb.host':'localhost',
                    'nokkhum.auth.secret':'nokkhum'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)
    
    def test_accountview_can_push_data_to_database(self):
        pp = pprint.PrettyPrinter(indent=4)
        
        args = dict(email       = 'test4@test.com', 
                    password    = '123456', 
                    first_name  = 'Boatty555', 
                    last_name   = '', 
                    )
        response = self.testapp.post_json('/accounts', params={'user':args}, status=200)
        print("response create: ")
        pp.pprint(response.json)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    unittest.main()
