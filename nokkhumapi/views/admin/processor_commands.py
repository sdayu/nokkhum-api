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
        compute_node = None
        if processor_command.compute_node:
            compute_node = dict(
                            id=processor_command.compute_node.id,
                            name=processor_command.compute_node.name  
                            )
        owner = None
        if processor_command.owner:
            owner = dict(
                      id=processor_command.owner.id,
                      email=processor_command.owner.email
                      )
            
        result = dict(
                        id=processor_command.id,
                        action=processor_command.action,
                        status=processor_command.status,
                        command_date=processor_command.command_date,
                        complete_date=processor_command.complete_date,
                        update_date=processor_command.update_date,
                        message=processor_command.message,
                        command_type=processor_command.command_type,
                        processor=dict(
                           id=processor_command.processor.id
                           ),
                        owner=owner,
                        compute_node=compute_node,
                        )
        return result
    
    @view_config(request_method="GET") 
    def get(self):
        processor_command_id = self.request.matchdict['processor_command_id']
        
        processor_command = models.ProcessorCommand.objects().with_id(processor_command_id)
        result = dict(
                    processor_command = self.build_processor_command(processor_command)
                )
        return result
    
    @view_config(route_name='admin.processor_commands.list', request_method="GET") 
    def list(self):
        processor_commands = models.ProcessorCommand.objects().order_by("-id").limit(20)
        
        result = dict(
                    processor_commands = [
                        self.build_processor_command(command)
                        for command in processor_commands
                        ]
                )

        return result