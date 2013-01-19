'''
Created on Jan 18, 2013

@author: boatkrap
'''
from ..interface import CameraDriver

class DLinkCamera(CameraDriver):
    def __init__(self, host, username, password, port=80):
        super().__init__(host, username, password, port)
        self.video_pattern = '/video/video.cgi'
        self.image_pattern = '/image.jpg'
    
    def get_video_url(self):
        url = super().get_base_url()+self.video_pattern
        return url
    
    def get_image_url(self):
        url = super().get_base_url()+self.image_pattern
        return url