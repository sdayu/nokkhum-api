'''
Created on Jan 18, 2013

@author: boatkrap
'''
from ..interface import CameraDriver

class AxisCamera(CameraDriver):
    def __init__(self, host, username, password, port=80):
        super().__init__(host, username, password, port)
        self.video_pattern = '/mjpg/video.mjpg'
        self.image_pattern = '/image/image.jpg'
        self.audio_pattern = '/audio.cgi'
    
    def get_video_uri(self):
        url = super().get_base_uri()+self.video_pattern
        return url
    
    def get_image_uri(self):
        url = super().get_base_uri()+self.image_pattern
        return url
    
    def get_audio_uri(self):
        url = super().get_base_uri()+self.audio_pattern
        return url