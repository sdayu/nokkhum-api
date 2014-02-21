'''
Created on Feb 3, 2014

@author: wongpiti
'''

from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

from nokkhumapi import models

@view_defaults(route_name='billing.default_service_plans', renderer='json', permission='role:admin')
class  DefaultServicePlan:
    def __init__(self, request):
        self.request = request
    
    @view_config(request_method='POST')  
    def set_default(self):
        matchdict = self.request.matchdict
        service_plan_id = matchdict.get('service_plan_id')
        the_service_plan = models.ServicePlan.objects(id=service_plan_id, status='active').first()
        service_plans = models.ServicePlan.objects(status='active').all()
        for service_plan in service_plans:
            if the_service_plan == service_plan:
                service_plan.default = True
            else:
                service_plan.default = False
                
            service_plan.save()
        
        sp = ServicePlan(self.request)
        
        return {'service_plan': sp.build_result(service_plan)}
        

@view_defaults(route_name='billing.service_plans', renderer='json', permission='authenticated')
class  ServicePlan:
    def __init__(self, request):
        self.request = request
    
    def build_result(self, service_plan):
        result = dict(
                      id = str(service_plan.id),
                      name = service_plan.name,
                      description = service_plan.description,
                      server_cost = service_plan.server_cost,
                      office_rent = service_plan.office_rent,
                      consume_cost = service_plan.consume_cost,
                      salary = service_plan.salary,
                      internet_service_charge = service_plan.internet_service_charge,
                      colocation_service_charge = service_plan.colocation_service_charge,
                      profit = service_plan.profit,
                      scaling_factor = service_plan.scaling_factor,
                      sell_price_per_minute = service_plan.sell_price_per_minute,
                      default = service_plan.default
                      )
        return result
        
    @view_config(route_name="billing.service_plans.create_list", request_method='POST')
    def create(self):
            service_plan_dict = self.request.json_body["service_plan"]
        
            service_plan = models.ServicePlan()    
            service_plan.name = service_plan_dict['name']
            service_plan.description = service_plan_dict['description']
            service_plan.server_cost = service_plan_dict['server_cost']
            service_plan.office_rent = service_plan_dict['office_rent']
            service_plan.consume_cost = service_plan_dict['consume_cost']
            service_plan.salary = service_plan_dict['salary']
            service_plan.internet_service_charge = service_plan_dict['internet_service_charge']
            service_plan.colocation_service_charge = service_plan_dict['colocation_service_charge']
            service_plan.profit = service_plan_dict['profit']
            service_plan.scaling_factor = service_plan_dict['scaling_factor']
            sell_price_per_minute = ((service_plan.server_cost/3/12/30/24/60) + ((service_plan.office_rent + service_plan.consume_cost \
                                                    + service_plan.salary + service_plan.internet_service_charge \
                                                    + service_plan.colocation_service_charge)/30/24/60)) \
                                                    +service_plan.profit
                                                    
            service_plan.sell_price_per_minute = round(sell_price_per_minute, 3)
            service_plan.save()
        
            service_plan.reload()
            service_plan_dict['id'] = str(service_plan.id)
            return {"service_plan":service_plan_dict}
    
    @view_config(route_name="billing.service_plans.create_list", request_method='GET')
    def list_service_plan(self):
        service_plans = models.ServicePlan.objects(status='active').all()
        
        results = dict(service_plans=[])
        for service_plan in service_plans:
            results['service_plans'].append(self.build_result(service_plan))
            
        return results
        
    
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        id = matchdict.get('service_plan_id')
        service_plan = models.ServicePlan.objects(id=id, status='active').first()
         
        return {'service_plan': self.build_result(service_plan)}
        
    @view_config(request_method='DELETE')
    def delete(self):
        matchdict = self.request.matchdict
        id = matchdict.get('service_plan_id')
        service_plan = models.ServicePlan.objects(id=id, status='active').first()
        if not service_plan:
            self.request.response.status = '404 Not Found'
            return {'result':"not found id : %s"%id}
        
        service_plan.status = 'delete'
        service_plan.save()
        
        return {'result':"Delete suscess"}
