'''
Created on Jul 11, 2012

@author: boatkrap
'''
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

from nokkhumapi import models

@view_defaults(route_name='admin.camera_running_fail', permission='r:admin', renderer='json')
class CameraRunningFail:
    def __init__(self, request):
        self.request = request
        
    @view_config(route_name='admin.camera_running_fail.list', request_method="GET")
    def list_camera(self):
        fail_status = models.CameraRunningFail.objects("-id").limit(30).all()
        return dict(
                    camera_running_fail=[
                                     dict(
                                          id=fs.id,
                                          camera=dict(
                                                      id=fs.camera.id
                                                      ),
                                          compute_node=dict(
                                                            id=fs.compute_node.id
                                                            ),
                                          report_time=fs.report_time,
                                          process_time=fs.process_time,
                                          message=fs.message
                                          )
                                     for fs in fail_status
                                     ]
                    )
        