'''
Created on Jan 18, 2013

@author: boatkrap
'''
from ..interface import CameraDriver

class DLinkCamera(CameraDriver):
    def __init__(self, host, username, password, port=80):
        super().__init__(host, username, password, port)
        self.video_pattern = '/video/mjpg.cgi'
        self.image_pattern = '/image/jpeg.cgi'
        self.audio_pattern = '/audio.cgi'
    
    def get_video_uri(self):
        uri = super().get_base_uri()+self.video_pattern
        return uri
    
    def get_image_uri(self):
        uri = super().get_base_uri()+self.image_pattern
        return uri
    
    def get_audio_uri(self):
        uri = super().get_base_uri()+self.audio_pattern
        return uri