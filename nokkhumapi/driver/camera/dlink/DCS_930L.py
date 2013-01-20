'''
Created on Jan 18, 2013

@author: boatkrap
'''

from .base_driver import DLinkCamera

class DLink_DCS_930L(DLinkCamera):
    
    def get_video_url(self, extension=''):
        url = super().get_video_url() + extension
        return url
    
    def get_image_url(self):
        url = super().get_image_url()
        return url