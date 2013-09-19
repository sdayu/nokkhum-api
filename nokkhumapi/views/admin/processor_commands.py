'''
Created on Sep 18, 2013

@author: boatkrap
'''
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.security import authenticated_userid

from nokkhumapi import models


@view_defaults(route_name='admin.processor_commands', permission='role:admin', renderer='json')
class ProcessorCommand:
    def __init__(self, request):
        self.request = request
        
    def build_processor_command(self, processor_command):
        result = dict(
                        id=processor_command.id,
                        action=processor_command.processor_command.action,
                        status=processor_command.processor_command.status,
                        command_date=processor_command.processor_command.command_date,
                        update_date=processor_command.processor_command.update_date,
                        message=processor_command.processor_command.message,
                        processor=dict(
                           id=processor_command.processor_command.processor.id
                           ),
                        owner=dict(
                          id=processor_command.processor_command.owner.id,
                          email=processor_command.processor_command.owner.email
                          ),
                        )
        return result
    
    @view_config(request_method="GET") 
    def get(self):
        processor_command_id = self.request.matchdict['processor_command_id']
        
        command = models.ProcessorCommandQueue.objects().with_id(processor_command_id)
        result = dict(
                    processor_command = self.build_processor_command(command)
                )
        
        return result