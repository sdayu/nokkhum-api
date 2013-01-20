'''
Created on Jan 18, 2013

@author: boatkrap
'''
from .dlink import driver as dlink_driver

class CameraDriverFactory:
    def get_camera_driver(self, manufactory):
        if manufactory == 'D-Link':
            return dlink_driver.DLinkDriverFactory()
        
    