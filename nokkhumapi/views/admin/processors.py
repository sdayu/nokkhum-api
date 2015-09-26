'''
Created on Sep 18, 2013

@author: boatkrap
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from dateutil import tz

from nokkhumapi import models


@view_defaults(route_name='admin.processors',
               permission='role:admin',
               renderer='json')
class Processor:
    def __init__(self, request):
        self.request = request

    def build_result(self, processor):
        if processor is None:
            return None

        processor_operating=dict(
                             user_command=processor.operating.user_command,
                             status=processor.operating.status,
                             updated_date=processor.operating.updated_date,
                             )
        if processor.operating.compute_node:
            compute_node = models.ComputeNode.objects.with_id(processor.operating.compute_node.id)
            processor_operating['compute_node']=dict(
                                               id=processor.operating.compute_node.id,
                                               )
            if compute_node:
                processor_operating['compute_node']['name'] = compute_node.name
            else:
                processor_operating['compute_node']['name'] = 'Unavailable'

        result = dict(
            id=processor.id,
            name=processor.name,
            storage_period=processor.storage_period,
            image_processors=processor.image_processors,
            created_date=processor.created_date,
            updated_date=processor.updated_date,
            status=processor.status,
            project=dict(
                id=processor.project.id,
                name=processor.project.name
                ),
            owner=dict(
                id=processor.owner.id,
                # email=processor.owner.email
                ),
            cameras=[dict(id=camera.id, name=camera.name) for camera in processor.cameras],
            processor_operating=processor_operating
            )
#         print('result:', result)
        return result

    @view_config(route_name='admin.processors.list', request_method='GET')
    def list_processor(self):
        if 'user_id' in self.request.GET:
            user = models.User.objects.with_id(self.request.GET.get('user_id'))
            processors = models.Processor.objects(owner=user, status='active').order_by('-operating__updated_date').all()
        else:
            processors = models.Processor.objects(status='active').order_by('-operating__updated_date').all()

        result = dict(
                processors=[ self.build_result(processor)
                  for processor in processors
                  ]
                )

        return result

    @view_config(request_method='GET')
    def get(self):
        processor_id = self.request.matchdict['processor_id']
        processor = models.Processor.objects().with_id(processor_id)

        result = dict(
                processor=self.build_result(processor)
                )

        return result

    @view_config(request_method='PUT')
    def update(self):
        matchdict = self.request.matchdict
        processor_id = matchdict.get('processor_id')

        processor = models.Processor.objects(id=processor_id).first()

        if not processor:
            self.request.response.status = '404 Not Found'
            return {}

        processor_dict = self.request.json_body["processor"]

        processor.name = processor_dict['name']
        processor.storage_period = processor_dict['storage_period']
        processor.image_processors = processor_dict['image_processors']

        processor.cameras = list()
        for camera_attribute in processor_dict['cameras']:
            camera = models.Camera.objects(id=camera_attribute['id']).first()
            processor.cameras.append(camera)

        processor.save()
        processor.reload()

        return dict(
                    processor=self.build_result(processor)
                    )


    @view_config(route_name='admin.processors.resources',
                 permission='admin',
                 request_method='GET')
    def get_resources(self):
        matchdict = self.request.matchdict
        processor_id = matchdict['processor_id']

        processor = models.Processor.objects.with_id(processor_id)

        processor_status = models.ProcessorStatus.objects(processor=processor)\
            .order_by('-id')\
            .limit(30)

        ctz = tz.tzlocal()
        resources = [
            dict(
                cpu=p.cpu,
                memory=p.memory,
                threads=p.threads,
                reported_date=p.reported_date.replace(tzinfo=ctz),
                messages=p.messages,
                ) for p in processor_status
            ]

        resources.reverse()

        return dict(
            resources=resources
        )
