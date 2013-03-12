from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.security import authenticated_userid

from nokkhumapi import models

@view_defaults(route_name='admin.compute_nodes', permission='r:admin', renderer="json")
class ComputeNode:
    def __init__(self, request):
        self.request = request
        
    @view_config(route_name='admin.compute_nodes.list', permission='r:admin', renderer='json')
    def list_compute_node(self):
        compute_nodes = models.ComputeNode.objects().all()
        return dict(
                    compute_nodes = [ dict(
                                           id=compute_node.id,
                                           name=compute_node.name
                                           )
                                     for compute_node in compute_nodes]
                    )
        
    @view_config(request_method="GET")
    def show(self):
        matchdict = self.request.matchdict
        compute_node_id = matchdict['compute_node_id']
        compute_node = models.ComputeNode.objects().with_id(compute_node_id)
        return dict(
                   compute_node=dict(
                                     id=compute_node.id,
                                     name=compute_node.name,
                                     update_date=compute_node.update_date,
                                     create_date=compute_node.create_date,
                                     host=compute_node.host,
                                     is_vm=compute_node.is_vm(),
                                     system=compute_node.system,
                                     machine=compute_node.machine,
                                     cpu=dict(
                                              count=compute_node.cpu.count,
                                              usage=compute_node.cpu.usage,
                                              usage_per_cpu=compute_node.cpu.usage_per_cpu
                                              ),
                                     memory=dict(
                                                total=compute_node.memory.total,
                                                used=compute_node.memory.used,
                                                free=compute_node.memory.free,
                                                 )
                                     )
                    )
    
    @view_config(request_method="DELETE")
    def delete(self):
        matchdict = self.request.matchdict
        compute_node_id = matchdict['compute_node_id']
        
        compute_node = models.ComputeNode.objects().with_id(compute_node_id)
        compute_node.delete()
        
