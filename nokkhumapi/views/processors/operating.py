'''
Created on Dec 26, 2012

@author: ww
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models
@view_defaults(route_name='processors.operating', renderer="json", permission="authenticated")
class ProcessorOperating(object):
    def __init__(self, request):
        self.request = request
    
    @view_config(request_method='POST')
    @view_config(request_method='PUT')
    def operate(self):
        matchdict   = self.request.matchdict
        processor_id = matchdict['processor_id']
    
        processor = models.Processor.objects(owner=self.request.user, id=processor_id).first()
        
        if not processor:
            self.request.response.status = '404 Not Found'
            return {'result':"camera not found id: %s"%processor_id}
        
        operating = self.request.json_body["processor_operating"]["action"]
        command_action  = 'no-command'
        user_command    = 'undefined'
        if operating == 'start':
            command_action = 'start'
            user_command = 'run'
        elif operating == 'stop':
            command_action = 'stop'
            user_command = 'suspend'
        
        pcq = models.ProcessorCommandQueue.objects(processor_command__owner=self.request.user, processor_command__processor=processor, processor_command__action=command_action).first()
        if pcq is not None:
            self.request.response.status = '406 Not Acceptable'
            return {'result':'processor name %s on operation' % processor.id}

        
#         camera.operating.status = command_action
        processor.operating.user_command = user_command
        processor.update_date = datetime.datetime.now()
        processor.save()
        
        pc          = models.ProcessorCommand()
        pc.command_date = datetime.datetime.now()
        pc.update_date = datetime.datetime.now()
        pc.action  = command_action
        pc.status  = 'waiting'
        pc.command_type = 'user'
        pc.processor  = processor
        pc.owner   = self.request.user
        
        pcq         = models.ProcessorCommandQueue()
        pcq.processor_command = pc
        pcq.save()
        pcq.reload()
        
        processor.operating.user_command_log.append(pcq.processor_command.id)
        processor.save()
        processor.reload()

        return dict(
                    processor_operating=dict(
                           action=pc.action,
                           id=pcq.id,
                           status=pc.status,
                           processor=dict(
                                     id=pc.processor.id                      
                                     ),
                            user=dict(
                                    id=pc.owner.id
                                    )
                           ),
                    result="success"
                )
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        processor_id = matchdict.get('processor_id')
        
        processor = models.Processor.objects(id=processor_id).first()

        if not processor:
            self.request.response.status = '404 Not Found'
            return {}
        result = dict(
                      processor_operating=dict(
                            status=processor.operating.status, 
                            update_date=processor.operating.update_date,
                            user_command=processor.operating.user_command,
#                                         compute_node={'id':camera.operating.compute_node._id}
                                
                            )
                      )
        
        return result
            
        
    
    
    
    
    
