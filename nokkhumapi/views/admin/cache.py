from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from pyramid.response import Response
from pyramid.security import authenticated_userid
import os

@view_defaults(route_name='admin.cache', permission='role:admin', renderer="json")
class Cache(object):
    def __init__(self, request):
        self.request = request
        
    @view_config(request_method="DELETE")
    def clear(self):
        cache_dir = self.request.registry.settings.get('nokkhum.temp_dir', None)
        if os.path.exists(cache_dir):    
            import shutil
            for name in os.listdir(cache_dir):
                shutil.rmtree(cache_dir+"/"+name)
                    
        
        return dict()
    
    @view_config(request_method="GET")
    def stat(self):
        
        cache_dir = self.request.registry.settings.get('nokkhum.temp_dir', None)
        if cache_dir is None or not os.path.exists(cache_dir):
            return dict(
                    cache =  dict(
                        cache_dir=False
                        )
                    )
            
        file_count  = 0
        for root, dirs, files in os.walk(cache_dir):
            for f in files:
                file_count += 1
        
        return dict(
                    cache =  dict(
                        cache_dir=True,
                        file_count=file_count
                        )
                    )