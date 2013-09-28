'''
Created on Jan 19, 2013

@author: boatkrap
'''

from .default import DefaultAxis


class AxisDriverFactory:
    def get_driver(self, model_name, **settings):
        return DefaultAxis(settings['host'], settings['username'], settings['password'], settings['port'])