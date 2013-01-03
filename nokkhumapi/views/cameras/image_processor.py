

from pyramid.view import view_defaults
from pyramid.view import view_config
from pyramid.response import Response

import json, datetime

from nokkhumapi import models

@view_config(route_name='cameras.image_processor', permission='authenticated', renderer='json')
class Prosessor(object):
    def __init__(self, request):
        self.request = request
    def processor(self):
        matchdict = self.matchdict
        camera_name = matchdict['name']
    
        camera = models.Camera.objects(owner=request.user, name=camera_name).first()
        
        if not camera:
            return Response('Camera not found')
        
        #import json
        form = camera_form.CameraProcessorForm(self.request.POST)
        
        if self.request.POST and form.validate():
            processors = json.loads(form.data['processors'])
        else:
            image_processors = models.ImageProcessor.objects().all()
            form.processors.data = json.dumps(camera.processors, indent=4)
            return dict(
                    image_processors=image_processors,
                    camera=camera, 
                    form=form
                    )
            
        camera.processors = processors
        camera.update_date = datetime.datetime.now()
        camera.save()
        
        return {}    






