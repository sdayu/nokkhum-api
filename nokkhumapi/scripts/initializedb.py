import os
import sys
import pymongo

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from .. import models

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    models.initial(settings)
    
    from ..security import SecretManager
    secret_manager = SecretManager(settings.get('nokkhum.auth.secret'))
    
    db_host = settings['mongodb.host']
    conn = pymongo.Connection(db_host)

    default_roles = ['admin', 'user']
    
    print ("begin to initial database")
    print ("initial default groups")
    for gname in default_roles:
        group = models.Role.objects(name=gname).first()
        if not group:
            group = models.Role()
            group.name = gname
            group.save()
    
    print ("initial admin user") 
    user = models.User.objects(email='admin@nokkhum.local').first()
    if not user:
        user = models.User()
        user.first_name = 'admin'
        user.last_name = ''
        user.password = secret_manager.get_hash_password('password')
        user.email = 'admin@nokkhum.local'
        role = models.Role.objects(name='admin').first()

        user.roles.append(role)

        user.save()
        
    user = models.User.objects(email='admin@nokkhum.local').first()
    
    print ("initial default manufatories and camera models")
    manufactories = {
                     'Generic': ['OpenCV'],
                     'D-Link':['DCS-930L']
                     }
   
    for manu_name in manufactories:
        
        man = models.Manufactory.objects(name=manu_name).first()
        if man is None:
            man = models.Manufactory()
            man.name = manu_name
            man.save()
        
        for cam_model_name in manufactories[manu_name]:
            camera_model = models.CameraModel.objects(name=cam_model_name, manufactory=man).first()
            if camera_model is None:
                camera_model = models.CameraModel()
                camera_model.name = cam_model_name
                camera_model.manufactory = man
                camera_model.save()
    
    print ("initial default image processors")
    processor_attributes = {
                            'Motion Detector':
                                {
                                    "motion_analysis_method" : "Optical Flow",
                                    "wait_motion_time" : 10,
                                    "name" : "Motion Detector",
                                    "interval" : 3,
                                    "region_of_interest" : "",
                                    "sensitive" : 90,
                                    "resolution" : 98,
                                    "enable_area_of_interest" : False,
                                    "processors" : [ ]
                                }
                                , 
                            'Face Detector':
                                {
                                    "interval" : 5,
                                    "name" : "Face Detector",
                                    "processors" : [ ]
                                }, 
                            'Video Recorder':
                                {
                                    "width" : 640,
                                    "record_motion" : False,
                                    "name" : "Video Recorder",
                                    "fps" : 10,
                                    "height" : 480
                                }, 
                            'Image Recorder':
                                {
                                    "width" : 640,
                                    "interval" : 1,
                                    "name" : "Image Recorder",
                                    "height" : 480
                                },
                            'Multimedia Recorder':
                                {
                                    "width" : 640,
                                    "name" : "Multimedia Recorder",
                                    "fps" : 10,
                                    "height" : 480
                                },
                            }
    
    for processor_name in processor_attributes:
        image_processor = models.ImageProcessor.objects(name=processor_name).first()
        
        if image_processor is None:
            image_processor = models.ImageProcessor()
            image_processor.name = processor_name
            
        image_processor.default_attributes = processor_attributes[processor_name]
        image_processor.save()
            
    print ("end initial database")