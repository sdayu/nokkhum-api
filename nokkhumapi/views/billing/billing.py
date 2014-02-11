'''
Created on Nov 27, 2013

@author: wongpiti
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import has_permission 

from nokkhumapi import models

from .. import resources


@view_defaults(route_name='billing.users', renderer='json', permission='authenticated')
class  Billing:
    def __init__(self, request):
        self.request = request


    @view_config(request_method='GET')
    def get(self):  
        matchdict = self.request.matchdict
        processor_id = matchdict.get('processor_id')
        
        self.request.GET['operation'] = 'AVG'
        
        user_resource = resources.user_resource.UserResource(self.request)
        processor_resource = user_resource.get()['processor_resource']
        
        total = 0
        
        service_plan = None
        if has_permission('role:admin', self.request.context, self.request):
            if 'service_plan' in self.request.GET:
                service_plan = models.ServicePlan.objects.with_id(self.request.GET.get('service_plan'))

        if service_plan is None:
            service_plan = models.ServicePlan.objects().first()
            
        if service_plan is None:
            service_plan = models.ServicePlan()
            service_plan.sell_price_per_minute = 1
            
        revenue = service_plan.sell_price_per_minute
        
        w1 = ((revenue * 0.7) / 8) / 100
        w2 = ((revenue * 0.3) / 0.5) * 10**-9 
        for resource in processor_resource['results']:
            price = (w1 * resource['cpu']) + (w2 * resource['ram']) 
            resource['price'] = price
            total += price
        
        del processor_resource['operation']
        processor_resource['total'] = round(total, 2)
        return dict(processor_billing = processor_resource)
        
        
        
        