'''
Created on Jan 19, 2013

@author: boatkrap
'''

from .base_driver import AxisCamera


class AxisDriverFactory:
    def get_driver(self, model_name, **settings):
        return AxisCamera(settings['host'], settings['username'], settings['password'], settings['port'])