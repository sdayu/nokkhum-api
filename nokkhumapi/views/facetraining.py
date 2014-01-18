'''
Created on Jan 15, 2014

@author: yoschanin.s
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

from os import walk
import shutil

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='facetraining', renderer="json", permission="authenticated")
class Facetraining(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        
        cameras = models.Camera.objects(owner=self.request.user).all()
        number = 0
        for camera in cameras:
            notifications = models.Notification.objects(camera=str(camera.id),status='False').all()
            number += len(notifications) 
                
        result = dict(
                      number=number
                    )
        
        return result
    
    @view_config(request_method='POST')
    def post(self):
        processor_dict = self.request.json_body["processor"]
        print('>>', processor_dict)
        processor = models.Processor()
        
        f = []
        mypath = '/home/superizer/Documents/myfacedb/face-' + self.request.user.face_id
        for dirnames in walk(mypath):
            f.extend(dirnames)
            break
        print('>>', f)
#         processor.name = processor_dict['name']
#         processor.storage_period = processor_dict['storage_period']
#         processor.image_processors = processor_dict['image_processors']
#         
#         
#         
#         processor.owner    = self.request.user
#         processor.project  = models.Project.objects(id=processor_dict["project"]["id"]).first()
#         
#         for camera_attribute in processor_dict['cameras']:
#             camera = models.Camera.objects(id=camera_attribute['id']).first()
#             processor.cameras.append(camera)
#    
#         processor.save()
#         processor.reload()
        
        return dict(
                    processor=self.build_result(processor)
                    )

