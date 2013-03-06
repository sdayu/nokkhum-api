'''
Created on Mar 6, 2013

@author: boatkrap
'''
from pyramid.view import view_defaults
from pyramid.view import view_config

from nokkhumapi import models

@view_defaults(route_name='image_processors', renderer="json", permission="authenticated")
class ProjectCamerasView:
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        image_processors = models.ImageProcessor.objects().all()
        
        return dict(
                image_processors=[dict(id=processor.id, name=processor.name)
                                  for processor in image_processors]
                )