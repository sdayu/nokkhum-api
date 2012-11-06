'''
Created on Oct 22, 2012

@author: coe
'''
import unittest


class TestProjectAPI(unittest.TestCase):


    def setUp(self):
        from .. import main
        settings = {'mongodb.db_name': 'nokkhum', 'mongodb.host': 'localhost'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)


    def tearDown(self):
        pass


    def test_project_create(self):
        args = dict(name='owen1', description='',)
        response = self.testapp.post_json('/projects', params={'project':args}, status=200)
        print("response create: ", response.json)
        
        self.assertIn("id", response.json["project"])
        
        self.project_id = response.json["project"]["id"]
        #test get
        response = self.testapp.get('/projects/%d'%self.project_id, status=200)
        print ("response get: ", response.json)
        
        self.assertEqual(response.json["project"]["id"], self.project_id)
        self.project_dict =  response.json["project"]
        
        self.assertIn("id", response.json["project"])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()