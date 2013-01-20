'''
Created on Jan 19, 2013

@author: boatkrap
'''

from .DCS_930L import DLink_DCS_930L


class DLinkDriverFactory:
    def get_driver(self, model, **settings):
        if model == 'DCS-930L':
            return DLink_DCS_930L(settings['host'], settings['username'], settings['password'], settings['port'])