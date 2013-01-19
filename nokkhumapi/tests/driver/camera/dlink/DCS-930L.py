'''
Created on Jan 18, 2013

@author: boatkrap
'''
import unittest

from nokkhumapi.driver.camera import factory
class DLink_DCS_930LTest(unittest.TestCase):

    def setUp(self):
        self.host = 'localhost'
        self.port = 80
        self.username = 'admin'
        self.password = 'adminpass'
        
        
    def test_get_url(self):
        
        fac = factory.CameraDriverFactory()
        
        settings = dict(
                        host=self.host,
                        port=self.port,
                        username=self.username,
                        password=self.password
                        )
        driver = fac.get_camera_driver('D-Link').get_driver("DCS-930L", **settings)
        
        print ('URL: ', driver.get_video_url())
        
        settings = dict(
                        host=self.host,
                        port=self.port,
                        username='',
                        password=''
                        )
        
        driver = fac.get_camera_driver('D-Link').get_driver("DCS-930L", **settings)
        print ('URL: ', driver.get_video_url())
        
        settings['port'] = 8080
        driver = fac.get_camera_driver('D-Link').get_driver("DCS-930L", **settings)
        print ('URL: ', driver.get_video_url(extension="?.mjpg"))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()