'''
Created on Nov 18, 2013

@author: wongpiti
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import mongoengine as me

import datetime
import math

from nokkhumapi import models
@view_defaults(route_name='user_resource', renderer='json', permission='authenticated')
class  UserResource:
    def __init__(self, request):
        self.request = request
     
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        processor_id = matchdict.get('processor_id')
        date_list = [int(d) for d in self.request.GET.get('start_date').split('-')]
        start_date = datetime.date(date_list[0], date_list[1], date_list[2]) 
        date_list = [int(d) for d in self.request.GET.get('end_date').split('-')]
        end_date = datetime.date(date_list[0], date_list[1], date_list[2])
        operation = self.request.GET.get('operation', 'max')
        processor = models.Processor.objects(id=processor_id, owner = self.request.user).first()
        
        processor_status = models.ProcessorStatus.objects(me.Q(report_date__gte = start_date) & me.Q(report_date__lt = end_date)
                                                          & me.Q(processor = processor)).all()
                           
#         print("start_processor_status :", processor_status[0])
#         print("end_processor_status :",processor_status[-1])
        
        resource_result = dict(
                      processor_resource=dict(
                          results = [],
                          start_date =  start_date,
                          end_date = end_date,
                          operation = operation.upper(),
                          processor=dict(id=processor_id)
                          )
                )
        
        if len(processor_status) == 0:
            return resource_result
        
        first_date = processor_status[0].report_date
        start_time = datetime.datetime(first_date.year, first_date.month, first_date.day, first_date.hour, first_date.minute)
        end_time = start_time + datetime.timedelta(minutes = 1)
        
        cpu = []
        ram = []
        results = []
        
        def build_result(start_date, cpu, ram):
            result = dict(report_date=start_time)
            if len(cpu) > 0:
                if (operation.upper() == 'AVG'):
                    #print("sample:", len(cpu))
                    result['cpu'] = round(sum(cpu)/len(cpu),2)
                    result['ram'] = round(sum(ram)/len(ram),2)
                else:
                    result['cpu'] = max(cpu)
                    result['ram'] = max(ram)
            else:
                result['cpu'] = 0
                result['ram'] = 0
                
            return result
                    
        for status in processor_status:
#             print("start time:", start_time)
#             print("report date:", status.report_date)
            if not (status.report_date >= start_time and status.report_date < end_time):
#                 print("new time")
                result = build_result(start_date, cpu, ram)
                    
                results.append(result)
                
                cpu = []
                ram = []

                next_date = status.report_date
                start_time = datetime.datetime(next_date.year, next_date.month, next_date.day, next_date.hour, next_date.minute)
                end_time = start_time + datetime.timedelta(minutes = 1)
                
            cpu.append(status.cpu)
            ram.append(status.memory)
        
        result = build_result(start_date, cpu, ram)
        results.append(result)
        
#         import pprint
#         pp = pprint.PrettyPrinter(indent=4)
#         print("results:")
#         pp.pprint(results)
        
        resource_result['processor_resource']['results'] = results
        
        return resource_result
    
        