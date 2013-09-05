'''
Created on Sep 5, 2013

@author: boatkrap
'''
import unittest
from nokkhumapi.driver.camera import factory

class AxisDriverTest(unittest.TestCase):


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
        driver = fac.get_camera_driver('Axis').get_driver("DCS-930L", **settings)
        print ('URL: ', driver.get_video_url())
        self.assertEqual('http://admin:adminpass@localhost/mjpg/video.mjpg', driver.get_video_url())
        
        settings = dict(
                        host=self.host,
                        port=self.port,
                        username='',
                        password=''
                        )
        
        driver = fac.get_camera_driver('Axis').get_driver("DCS-930L", **settings)
        print ('URL: ', driver.get_video_url())
        self.assertEqual('http://localhost/mjpg/video.mjpg', driver.get_video_url())
        
        settings['port'] = 8080
        driver = fac.get_camera_driver('Axis').get_driver("DCS-930L", **settings)
        print ('URL: ', driver.get_video_url())
        self.assertEqual('http://localhost:8080/mjpg/video.mjpg', driver.get_video_url())
        
        settings = dict(
                        host=self.host,
                        port=self.port,
                        username='admin',
                        password='admin@nokkhum'
                        )
        driver = fac.get_camera_driver('Axis').get_driver("DCS-930L", **settings)
        print ('URL: ', driver.get_video_url())
        self.assertEqual('http://admin:admin%40nokkhum@localhost/mjpg/video.mjpg', driver.get_video_url())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()