'''
Created on Jan 15, 2014

@author: yoschanin.s
'''
from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='notifications', renderer="json", permission="authenticated")
class Notification(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method='GET')
    def get(self):
        
        cameras = models.Camera.objects(owner=self.request.user).all()
        result = dict(
                      new=[],
                      old=[]
                    )
        for camera in cameras:
            notifications = models.Notification.objects(camera=str(camera.id), status='False').all()
            for notification in notifications:
                names = models.Facetraining.objects(faceid=str(notification.face_name[5:]), owner=self.request.user).first()
                print('>>' , names, notification.face_name[5:])
                if names is None:
                    names.name = notification.face_name
                result['new'].append(
                                     dict(
                                          id=notification.id,
                                          camera=dict(
                                                      name=camera.name
                                                      ),
                                          method=notification.method,
                                          filename=notification.filename,
                                          face_name=names.name,
                                          description=notification.description,
                                          create_date=notification.create_date
                                          )
                                     )
            notifications = models.Notification.objects(camera=str(camera.id), status='True').all()
            for notification in notifications:
                names = models.Facetraining.objects(faceid=str(notification.face_name[5:]), owner=self.request.user).first()
                print('>>' , names, notification.face_name[5:])
                if names is None:
                    names.name = notification.face_name
                result['old'].append(
                                     dict(
                                          camera=dict(
                                                      name=camera.name
                                                      ),
                                          method=notification.method,
                                          filename=notification.filename,
                                          face_name=names.name,
                                          description=notification.description,
                                          create_date=notification.create_date
                                          )
                                     )
        return dict(
                    notifications=result
                    )
        
    @view_config(request_method='POST')   
    def create(self):
        notifications = self.request.json_body["notifications"]
        for notification in notifications:
            noti = models.Notification.objects(id=notification['id']).first()
            noti.status = 'True'
            noti.save()
        return {}
