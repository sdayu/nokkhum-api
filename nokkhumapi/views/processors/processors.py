'''
Created on Sep 12, 2013

@author: boatkrap
'''

from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='processors.processors', renderer="json", permission="authenticated")
class ProcessorView(object):
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
    
    @view_config(route_name="processors.create_list", request_method='GET')
    def list_processors(self):
        matchdict = self.request.matchdict
        project_id = matchdict.get('project_id')
        
        processors = models.Processor.objects(owner=self.request.user, project__id=project_id).all()
         
        results = dict(processors=list())
        for processor in processors:
            results['processors'].append(self.build_result(processor))
         
        return results
    
    @view_config(route_name="processors.create_list", request_method='POST')
    def create(self):
        processor_dict = self.request.json_body["processor"]

        processor = models.Processor()
        processor.name = processor_dict['name']
        processor.storage_period = processor_dict['storage_period']
        processor.image_processors = processor_dict['image_processors']
        
        processor.owner    = self.request.user
        processor.project  = models.Project.objects(id=processor_dict["project"]["id"]).first()
        
        for camera_attribute in processor_dict['cameras']:
            camera = models.Camera.objects(id=camera_attribute['id']).first()
            processor.cameras.append(camera)
        
        print("input create:", processor_dict)
        processor.save()
        processor.reload()
        
        return dict(
                    processor=self.build_result(processor)
                    )
        
    @view_config(request_method='PUT')
    def update(self):
        matchdict = self.request.matchdict
        processor_id = matchdict.get('processor_id')
        
        processor = models.Processor.objects(id=processor_id, owner=self.request.user).first()
        
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
        
    @view_config(request_method='GET')
    def get(self):
        matchdict = self.request.matchdict
        processor_id = matchdict.get('processor_id')
        
        processor = models.Processor.objects(id=processor_id, owner=self.request.user).first()
        
        if not processor:
            self.request.response.status = '404 Not Found'
            return {}
        
        return dict(
                    processor=self.build_result(processor)
                    )
    
    @view_config(request_method='DELETE')
    def delete(self):
        matchdict = self.request.matchdict
        processor_id = matchdict.get('processor_id')
        
        processor = models.Processor.objects(id=processor_id, owner=self.request.user).first()
        
        if not processor:
            self.request.response.status = '404 Not Found'
            return {}
        
        processor.delete()
        
        return {}
    
    