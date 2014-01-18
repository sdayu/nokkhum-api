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
    
    def build_result(self, processor):
        processor_operating=dict(
                             user_command=processor.operating.user_command,
                             status=processor.operating.status,
                             update_date=processor.operating.update_date,
                             )
        if processor.operating.compute_node:
            processor_operating['compute_node']=dict(
                                               id=processor.operating.compute_node.id
                                               )
            try:
                processor_operating['compute_node']['name']=processor.operating.compute_node.name
            except:
                pass
            
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
        mypath = '/home/superizer/Documents/myfacedb'
        for dirnames in walk(mypath):
            f.extend(dirnames)
            break
        print('>>', f)
        face_name = models.Facetraining.objects(name=processor_dict['name'], owner=self.request.user).first()
        if face_name is None:
            face_name = models.Facetraining()
            face_name.name = processor_dict['name']
            face_name.owner = self.request.user
            face_name.faceid = str(len(f[1]))
            face_name.save()
            
        else:
            print('>>', 'face-' + face_name.faceid, mypath + '/face-' + face_name.faceid)
            if 'face-' + face_name.faceid in f[1]:
                shutil.rmtree(mypath + '/face-' + face_name.faceid)
    
        processor_dict['image_processors'][0]['face_id'] = face_name.faceid
        processor = models.Processor()
        processor.name = processor_dict['name']
        processor.storage_period = processor_dict['storage_period']
        processor.image_processors = processor_dict['image_processors']
        
        processor.owner    = self.request.user
        processor.project  = models.Project.objects(id=processor_dict["project"]["id"]).first()
         
        for camera_attribute in processor_dict['cameras']:
            camera = models.Camera.objects(id=camera_attribute['id']).first()
            processor.cameras.append(camera)
    
        processor.save()
        processor.reload()
        
        return dict(
                    processor=self.build_result(processor)
                    )

