'''
Created on Jan 18, 2013

@author: boatkrap
'''

from .base_driver import DLinkCamera

class DLink_DCS_930L(DLinkCamera):
    
    def get_video_uri(self, extension=''):
        url = super().get_video_uri() + extension
        return url
    
    def get_image_uri(self):
        url = super().get_image_uri()
        return url