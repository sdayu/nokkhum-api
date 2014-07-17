from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.security import authenticated_userid

from nokkhumapi import models


@view_defaults(route_name='admin.compute_nodes', permission='role:admin', renderer="json")
class ComputeNode:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='admin.compute_nodes.list', permission='role:admin', renderer='json')
    def list_compute_node(self):
        compute_nodes = models.ComputeNode.objects().order_by("-updated_date").all()
        result = dict(
            compute_nodes=[dict(
                id=compute_node.id,
                name=compute_node.name
                )
                for compute_node in compute_nodes]
            )

        return result

    @view_config(request_method="GET")
    def show(self):
        matchdict = self.request.matchdict
        compute_node_id = matchdict['compute_node_id']
        compute_node = models.ComputeNode.objects().with_id(compute_node_id)
        if not compute_node:
            return dict(compute_node=dict(
                                          host='Unavailable'
                                          ))
        return dict(
            compute_node=dict(
                id=compute_node.id,
                name=compute_node.name,
                updated_date=compute_node.updated_date,
                created_date=compute_node.created_date,
                updated_resource_date=compute_node.updated_resource_date,
                host=compute_node.host,
                is_vm=compute_node.is_vm(),
                online=compute_node.is_online(),
                system=compute_node.system,
                machine=compute_node.machine,
                cpu=dict(
                    count=compute_node.cpu.count,
                    used=compute_node.cpu.used,
                    used_per_cpu=compute_node.cpu.used_per_cpu
                    ),
                memory=dict(
                    total=compute_node.memory.total,
                    used=compute_node.memory.used,
                    free=compute_node.memory.free,
                    ),
                disk=dict(
                    total=compute_node.disk.total,
                    used=compute_node.disk.used,
                    free=compute_node.disk.free,
                    ),
                extra=compute_node.extra
                )
            )

    @view_config(request_method="DELETE")
    def delete(self):
        matchdict = self.request.matchdict
        compute_node_id = matchdict['compute_node_id']

        compute_node = models.ComputeNode.objects().with_id(compute_node_id)
        compute_node.delete()

    @view_config(route_name='admin.compute_nodes.processors',
                 permission='admin',
                 request_method='GET')
    def get_processors(self):
        matchdict = self.request.matchdict
        compute_node_id = matchdict['compute_node_id']

        compute_node = models.ComputeNode.objects().with_id(compute_node_id)
        processors = models.Processor.objects(operating__compute_node=compute_node).all()

        return dict(
            processors=[dict(
                id=processor.id,
                name=processor.name
            ) for processor in processors]
        )


@view_defaults(route_name='admin.compute_nodes.vm', permission='role:admin', renderer="json")
class VM:
    def __init__(self, request):
        self.request = request

    @view_config(request_method="GET")
    def show(self):
        matchdict = self.request.matchdict
        compute_node_id = matchdict['compute_node_id']
        compute_node = models.ComputeNode.objects().with_id(compute_node_id)

        if not compute_node or compute_node.vm is None:
            return dict(vm=None)
        return dict(
            vm=dict(
                id=compute_node.id,
                name=compute_node.vm.name,
                image_id=compute_node.vm.image_id,
                instance_id=compute_node.vm.instance_id,
                instance_type=compute_node.vm.instance_type,
                ip_address=compute_node.vm.ip_address,
                private_ip_address=compute_node.vm.private_ip_address,
                started_instance_date=compute_node.vm.started_instance_date,
                status=compute_node.vm.status,
                extra=compute_node.vm.extra
            )
        )
