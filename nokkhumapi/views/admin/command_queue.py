from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.security import authenticated_userid

from nokkhumapi import models


@view_defaults(route_name='admin.command_queue', permission='role:admin', renderer='json')
class ProcessorCommandQueue:
    def __init__(self, request):
        self.request = request
    
    def build_processor_command_queue(self, command_queue):
        owner = None
        
        if command_queue.processor_command.owner:
            owner=dict(
                       id=command_queue.processor_command.owner.id
                    )
        
        result = dict(
                       id=command_queue.id,
                       processor_command=dict(
                            id=command_queue.processor_command.id,
                            processor=dict(
                                id=command_queue.processor_command.processor.id,
                                name=command_queue.processor_command.processor.name
                            ),
                            owner=owner
                        )
                    )
        return result
    
    @view_config(route_name='admin.command_queue.list', request_method="GET")
    def list_command(self):
        processor_command_queue = models.ProcessorCommandQueue.objects().order_by("+id").all()
        result = dict(
                    processor_command_queue=[
                        self.build_processor_command_queue(command)
                        for command in processor_command_queue]
                    )
        return result
        
        
    @view_config(request_method="GET")
    def get(self):
        matchdict = self.request.matchdict
        command_id = matchdict['command_id']
        command = models.ProcessorCommandQueue.objects().with_id(command_id)

        return dict(
                    processor_command_queue=self.build_processor_command_queue(command)
                    )