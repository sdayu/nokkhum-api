'''
Created on Oct 22, 2012

@author: coe
'''
import unittest
import pprint

class TestProjectAPI(unittest.TestCase):


    def setUp(self):
        from .. import main
        settings = {'mongodb.db_name': 'nokkhum', 
                    'mongodb.host': 'localhost',
                    'nokkhum.auth.secret': 'nokkhum'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)


    def tearDown(self):
        pass


#    def test_project_create(self):
#        args = dict(name='owen1', description='',)
#        response = self.testapp.post_json('/projects', params={'project':args}, status=200)
#        print("response create: ", response.json)
#        
#        self.assertIn("id", response.json["project"])
#        
#        self.project_id = response.json["project"]["id"]
#        #test get
#        response = self.testapp.get('/projects/%d'%self.project_id, status=200)
#        print ("response get: ", response.json)
#        
#        self.assertEqual(response.json["project"]["id"], self.project_id)
#        self.project_dict =  response.json["project"]
#        
#        self.assertIn("id", response.json["project"])
    def test_projectview_can_push_data_to_database(self):
        pp=pprint.PrettyPrinter(indent=4)
        #create project
        args=dict(
                  name = 'JoJo',
                  description = '',
                  status = 'Active',
                  user = {"id":1}
                )
        response = self.testapp.post_json('/projects', params={'project':args}, status=200)
        print("responce post :")
        pp.pprint(response.json)
        
        self.assertIn("id",response.json["project"])
        
        self.project_id = response.json["project"]["id"]
        
        #retrieve project via project id
        response = self.testapp.get('/projects/%d'%self.project_id, status = 200)
        print("response get")
        pp.pprint(response.json)
        
        self.assertEqual(response.json["project"]["id"], self.project_id)
        self.project_dict =  response.json["project"]
        
        #try to change name
        self.project_dict['status'] = 'Delete'
        args = self.project_dict
        
        response = self.testapp.put_json('/projects/%d'%response.json["project"]["id"], params={'project':args}, status=200)
        print("response update: ")
        pp.pprint(response.json)
        
        self.assertIn("id", response.json["project"])
        
        response = self.testapp.delete('/projects/%d'%response.json["project"]["id"], status=200)
        print("response delete: ")
        pp.pprint(response.json)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()