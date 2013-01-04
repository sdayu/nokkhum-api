from pyramid.httpexceptions import HTTPFound

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.response import Response, FileResponse
from pyramid.security import authenticated_userid

from .. import models

import os
import urllib

@view_defaults(permission="authenticated", route_name="storage")
class Storage:
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method="GET", renderer="json")
    def storage_list(self):
        s3_client = self.request.s3_client
        file_list = []
        matchdict = self.request.matchdict
        extension = matchdict['extension']

        if len(extension) == 0 or extension == "/":
            cameras = models.Camera.objects(owner=self.request.user).all()
            for camera in cameras:
                item = dict(
                            name=str(camera.id),
                            file=False,
                            url=urllib.parse.unquote(self.request.route_path('storage', extension="/%d"%camera.id))
                            )
                file_list.append(item)
        else:
            uri = extension[1:]
            end_pos = uri.find("/")
            if end_pos > 0:
                camera_id = uri[:end_pos]
            else:
                camera_id = uri
    #        print "camera name: ", camera_name
            camera = models.Camera.objects(owner=self.request.user, id=camera_id).first()
    
            s3_client.set_buckket_name(int(camera.id))
    
            prefix = ""
            if len(uri[end_pos+1:]) > 0 and uri[end_pos+1:] != camera_id:
                prefix = "%s/" % (uri[end_pos+1:])
    
            for s3_item in s3_client.list_file(prefix):
                start_pos = s3_item.rfind("/")
    
                path = s3_item
                    
                file_extension = ""
                pos = path.rfind(".")
                if pos > 0:
                    file_extension = path[pos:]
                    if file_extension not in [".jpg", ".png", ".avi", ".webm", ".webp", ".ogg", ".ogv"]:
                        file_extension = ""
                
                download_link = None
                if len(file_extension) > 0:
                    download_link = self.request.route_url('storage.download', extension="/%d/%s"%(camera.id, path))
                
                view_link = self.request.route_path('storage', extension="/%d/%s"%(camera.id, path))
                
                item = dict(
                            name = s3_item[start_pos+1:], 
                            url = urllib.parse.unquote(view_link),
                            file = False
                            )
                if download_link is not None:
                    item['download'] = urllib.parse.unquote(download_link)
                    item['file'] = True
                    
                file_list.append(item)
        return dict(
                    files=file_list,
                    )
        
    @view_config(request_method="DELETE", renderer="json")
    def delete(self):
        matchdict = self.request.matchdict
        extension = matchdict['extension']
        
        uri = extension[1:]
        end_pos = uri.find("/")
        if end_pos > 0:
            camera_id = uri[:end_pos]
        else:
            camera_id = uri
        
        camera = models.Camera.objects(owner=self.request.user, id=camera_id).first()
        if camera is None:
            self.request.response.status = '404 Not Found'
            return {'result':'file not found'}
        
        key_name = "%s"%(uri[end_pos+1:])
        
        s3_client = self.request.s3_client
        s3_client.set_buckket_name(int(camera.id))
        s3_client.delete(key_name)
        return {'result':'delete success'}
        
    def cache_file(self, request):
        cache_dir = request.registry.settings['nokkhum.temp_dir']
        matchdict = request.matchdict
        extension = matchdict['extension']
        
        user = request.user
        
        camera_id = ""
        
        uri = extension[1:]
        end_pos = uri.find("/")
        if end_pos > 0:
            camera_id = uri[:end_pos]
        else:
            camera_id = uri
        
        camera = models.Camera.objects(owner=request.user, id=camera_id).first()
        if camera is None:
            return None
        
        key_name = "%s"%(uri[end_pos+1:])
        container_dir = "%s/%d/%s"%(cache_dir, camera.id, key_name[:key_name.rfind("/")])
        file_name = "%s/%d/%s"%(cache_dir, camera.id, key_name)
        
        s3_client = self.request.s3_client
        s3_client.set_buckket_name(int(camera.id))
    
        if not s3_client.is_avialabel(key_name):
            return None
    
        if os.path.exists(file_name):
            return file_name
        
        if not os.path.exists(container_dir):
            try:
                os.makedirs(container_dir)
            except:
                pass
    
    #    print "key_name: ", key_name
    #    print "file_name: ", file_name
        s3_client.get_file(key_name, file_name)
        
        return file_name
                            
    
    @view_config(route_name='storage.download', request_method="GET")
    def download(self):
    
        file_name = self.cache_file(self.request)
    
        if file_name is None:
            self.request.response.status = '404 Not Found'
            return self.request.response
        
        #matchdict = self.request.matchdict
        #fizzle = matchdict['fizzle']
        
        response = FileResponse(file_name, request=self.request, content_encoding=None)
        
        response.content_encoding = None
        
        return response
    
    
    
#    @view_config(route_name='storage.view'request_method="GET")
#    def view(self):
#        matchdict = self.request.matchdict
#        fizzle = matchdict['extension']
#        
#        file_type="unknow"
#        extension = fizzle[fizzle.rfind("."):]
#        if extension in [".png", ".jpg", ".jpeg"]:
#            file_type="image"
#        elif extension in [".avi", ".ogg", ".ogv", ".mpg", ".webm"]:
#            file_type="video"
#    
#        url         = self.request.route_path("storage.download", fizzle=fizzle)
#        delete_url  = self.request.route_path("storage.delete", fizzle=fizzle)
#        
#    
#        return dict (
#                     file_type=file_type,
#                     url=urllib.request.url2pathname(url),
#                     delete_url=urllib.request.url2pathname(delete_url),
#                     )