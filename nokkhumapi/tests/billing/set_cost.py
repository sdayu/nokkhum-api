'''
Created on Feb 4, 2014

@author: wongpiti
'''
import unittest
import pprint

class ProcessorTest(unittest.TestCase):

    def setUp(self):
        from nokkhumapi import main
        from webtest import TestApp
        
        settings = {'mongodb.db_name': 'nokkhum', 
                    'mongodb.host': '172.30.235.111',
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
    
    def test_create_service_plan(self):
        args = dict(
                name='test service plan name',
                description='test',
                server_cost = 1,
                office_rent = 1,
                consume_cost = 1,
                salary = 1,
                internet_service_charge = 1,
                colocation_service_charge = 1,
                profit = 1
                )
        print('service plan args:')
        self.pp.pprint(args)
        response = self.testapp.post_json('/billing/service_plans', params={'service_plan':args}, headers=[('X-Auth-Token', self.token)], status=200)
        service_plan = response.json['service_plan']
        print('add service plan')
        self.pp.pprint(service_plan)
        
        self.assertIn('id', service_plan)

    def test_list_service_plan(self):
        ''''''
        response = self.testapp.get('/billing/service_plans', headers=[('X-Auth-Token', self.token)])
        
        print("list service plan: ")
        self.pp.pprint(response.json)
        
    def test_get_service_plan(self):
        response = self.testapp.get('/billing/service_plans', headers=[('X-Auth-Token', self.token)])
        service_plans = response.json['service_plans']
        response = self.testapp.get('/billing/service_plans/%s'%service_plans[0]['id'], headers=[('X-Auth-Token', self.token)])
        service_plan = response.json['service_plan']
        print('get service plan id:', service_plan['id'])
        self.pp.pprint(service_plan)
      
    def test_delete_service_plan(self):
        response = self.testapp.get('/billing/service_plans', headers=[('X-Auth-Token', self.token)])
        service_plans = response.json['service_plans']
        
        print("delete id:", service_plans[0]['id'])
        response = self.testapp.delete('/billing/service_plans/%s'%service_plans[0]['id'], headers=[('X-Auth-Token', self.token)])
        print('delete', response)
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    