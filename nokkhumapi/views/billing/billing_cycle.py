'''
Created on Jan 18, 2014


'''
import datetime
import calendar


from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

from nokkhumapi import models

from .. import resources


@view_defaults(route_name='billing.billing_cycle', renderer='json', permission='authenticated')
class  BillingCycle:
    def __init__(self, request):
        self.request = request


    @view_config(request_method='GET')
    def get(self):  
        matchdict = self.request.matchdict
        processor_id = matchdict.get('processor_id')
        
        processor = models.Processor.objects.with_id(processor_id)
        start_processor_status = models.ProcessorStatus.objects(processor = processor).order_by('+report_date').first()
        end_processor_status = models.ProcessorStatus.objects(processor = processor).order_by('-report_date').first()
        
        results = []
        
        started_date = start_processor_status.report_date.date()
        while(True):
            
            
            finished_date = datetime.date(started_date.year, started_date.month, calendar.monthrange(started_date.year, started_date.month)[1])
            
            result = dict(started_date=started_date, finished_date=finished_date)
            results.append(result)
            
            if finished_date > end_processor_status.report_date.date():
                result['finished_date'] = end_processor_status.report_date.date()
                break
            else:
                started_date = finished_date + datetime.timedelta(days=1)
        
        return dict(
                    billing_cycle=results
                    )