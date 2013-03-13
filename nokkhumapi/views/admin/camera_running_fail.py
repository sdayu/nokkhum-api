'''
Created on Jul 11, 2012

@author: boatkrap
'''
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from pyramid.response import Response

@view_defaults(route_name='admin.camera_running_fail', permission='r:admin', renderer='json')
class CameraRunningFail:
    def __init__(self, request):
        self.request = request
        
    @view_config(route_name='admin.camera_running_fail.list', request_method="GET")
    def list_camera(self):
        fail_status = models.CameraRunningFail.objects("-id").limit("30").all()
        return dict(
                    run_fail_status=[]
                    )
        