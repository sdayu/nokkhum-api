'''
Created on Sep 18, 2013

@author: boatkrap
'''
from pyramid.view import view_defaults
from pyramid.view import view_config

from nokkhumapi import models

@view_defaults(route_name='admin.processors', permission='role:admin', renderer='json')
class Processor:
    def __init__(self, request):
        self.request = request
        
    def build_result(self, processor):
        processor_operating=dict(
                             user_command=processor.operating.user_command,
                             status=processor.operating.status,
                             update_date=processor.operating.update_date,
                             )
        if processor.operating.compute_node:
            processor_operating['compute_node']=dict(
                                               id=processor.operating.compute_node.id,
                                               name=processor.operating.compute_node.name
                                               )
        result = dict(
                      id=processor.id,
                      name=processor.name,
                      storage_period=processor.storage_period,
                      image_processors=processor.image_processors,
                      create_date=processor.create_date,
                      update_date=processor.update_date,
                      status=processor.status,
                      project=dict(
                            id=processor.project.id,
                            name=processor.project.name
                            ),
                      owner=dict(
                            id=processor.owner.id,
                            email=processor.owner.email
                            ),
                      cameras=[dict(id=camera.id, name=camera.name) for camera in processor.cameras],
                      processor_operating=processor_operating
                      )
#         print("result:", result)
        return result
    
    @view_config(route_name="admin.processors.list")
    def list_processor(self):
        processors = models.Processor.objects().all()
        result = dict(
                processors=[ self.build_result(processor)
                  for processor in processors
                  ]   
                )
        
        return result