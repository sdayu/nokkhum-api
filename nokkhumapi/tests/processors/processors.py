'''
Created on Sep 13, 2013

@author: boatkrap
'''
import unittest
import pprint

class ProcessorTest(unittest.TestCase):

    def setUp(self):
        from nokkhumapi import main
        from webtest import TestApp
        
        settings = {'mongodb.db_name': 'nokkhum', 
                    'mongodb.host': 'localhost',
                    'nokkhum.auth.secret': 'nokkhum'}
        
        app = main({}, **settings)
        self.testapp = TestApp(app)
        
        args = dict(password_credentials= {"username": "admin@nokkhum.local", 
                                          "password": "password"}
                    )
        
        response = self.testapp.post_json('/authentication/tokens', params=args, status=200)
        
        self.pp=pprint.PrettyPrinter(indent=4)
        self.pp.pprint(response.json)
        
        self.token = response.json['access']['token']['id']
        self.user_id = response.json['access']['user']['id']
        
        user_projects = self.testapp.get('/users/%s/projects'%self.user_id, headers=[('X-Auth-Token', self.token)], status=200)
        self.project_id = user_projects.json['projects'][0]['id']

    def tearDown(self):
        pass

    
        
    def test_add_processor(self):
        response = self.testapp.get('/projects/%s/cameras'%self.project_id, headers=[('X-Auth-Token', self.token)], status=200)
        
        camera = response.json['cameras'][0]
        args = dict(
                name='test processor name',
                storage_period=12,
                image_processors=list(),
                cameras=[dict(id=camera['id'])],
                project=dict(id=self.project_id),
                )
        print('processor args:')
        self.pp.pprint(args)
        response = self.testapp.post_json('/processors', params={'processor':args}, headers=[('X-Auth-Token', self.token)], status=200)
        processor = response.json['processor']
        print('add processor')
        self.pp.pprint(processor)
        
        self.assertIn('id', processor)
        
    def test_list_processors(self):
        ''''''
        response = self.testapp.get('/projects/%s/processors'%self.project_id, headers=[('X-Auth-Token', self.token)])
     
        print("list project: ")
        self.pp.pprint(response.json)
        
    def test_get_processor(self):
        response = self.testapp.get('/projects/%s/processors'%self.project_id, headers=[('X-Auth-Token', self.token)])
        processors = response.json['processors']
        if len(processors) == 0:
            print('processor none')
            return
            
        response = self.testapp.get('/processors/%s'%processors[0]['id'], headers=[('X-Auth-Token', self.token)], status=200)
        processor = response.json['processor']
        print('get processor id:', processors[0]['id'])
        self.pp.pprint(processor)
        
        self.assertIn('id', processor)
        self.assertEqual(processors[0]['id'], processor['id'])

    def test_delete_processor(self):
        response = self.testapp.get('/projects/%s/processors'%self.project_id, headers=[('X-Auth-Token', self.token)])
        processors = response.json['processors']
        if len(processors) == 0:
            print('processor none')
            return
            
        response = self.testapp.delete('/processors/%s'%processors[0]['id'], headers=[('X-Auth-Token', self.token)], status=200)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()