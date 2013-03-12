from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.security import authenticated_userid

from nokkhumapi import models

@view_defaults(route_name='admin.command_log', permission='r:admin', renderer='json')
class CommandLog:
    def __init__(self, request):
        self.request = request
        
    @view_config(route_name='admin.command_log.list', permission='r:admin', renderer='json')
    def list_command(self):
        command_log = models.CommandLog.objects().order_by("-id").limit(30)
        return dict(
                    command_log = [dict(
                                        id=cl.id,
                                        attributes=cl.attributes,
                                        action=cl.action,
                                        command_date=cl.command_date,
                                        complete_date=cl.complete_date,
                                        status=cl.status,
                                        message=cl.message,
                                        compute_node=dict(
                                                          id=cl.compute_node.id,
                                                          name=cl.compute_node.name
                                                          ),
                                        owner=dict(
                                                   id=cl.owner.id,
                                                   email=cl.owner.email
                                                   )
                                        )
                                   for cl in command_log]
                    )