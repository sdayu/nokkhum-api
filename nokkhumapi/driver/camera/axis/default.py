'''
Created on Jan 18, 2013

@author: boatkrap
'''

from .base_driver import AxisCamera

class DefaultAxis(AxisCamera):
    
    def get_video_uri(self):
        url = super().get_video_uri()
        return url
    
    def get_image_uri(self):
        url = super().get_image_uri()
        return url