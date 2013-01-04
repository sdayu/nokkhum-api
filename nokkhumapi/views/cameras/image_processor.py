

from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_defaults(route_name='cameras.image_processor', permission='authenticated', renderer='json')
class Prosessor(object):
    def __init__(self, request):
        self.request = request
    
    @view_config(request_method=('POST', 'PUT'))
    def processor(self):
        matchdict = self.request.matchdict
        camera_id = matchdict['camera_id']
    
        camera = models.Camera.objects(owner=self.request.user, id=camera_id).first()
        
        if not camera:
            self.request.response.status = '404 Not Found'
            return {'result':"not found id: %d"%camera_id}
        

        processors = self.request.json_body['processors']

            
        camera.processors = processors
        camera.update_date = datetime.datetime.now()
        camera.save()
        
        return dict(
                    camera=dict(
                                id=camera.id,
                                name=camera.name,
                                processors=processors
                                )
                    
                    )   






