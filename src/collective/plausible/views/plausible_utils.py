# -*- coding: utf-8 -*-

from collective.plausible.utils import get_plausible_infos
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface

import requests


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IPlausibleUtilsView(Interface):
    """Marker Interface for IPlausibleUtilsView"""


@implementer(IPlausibleUtilsView)
class PlausibleUtilsView(BrowserView):

    def is_plausible_set(self):
        # __import__("pdb").set_trace()
        return True if get_plausible_infos(self) else False

    def add_link_user_action(self):
        # __import__("pdb").set_trace()
        return getattr(get_plausible_infos(self), "plausible_link_object_action", False)

    @property
    def get_plausible_instance_healthcheck(self):
        vars = get_plausible_infos(self)
        try:
            response = requests.get(f"https://{vars['plausible_url']}/api/health")
            return response.json()
        except:
            return False
