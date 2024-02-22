# -*- coding: utf-8 -*-

import requests

from collective.plausible.utils import get_plausible_vars
from zope.interface import Interface
from plone import api
from Products.Five.browser import BrowserView
from zope.interface import implementer


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IPlausibleUtilsView(Interface):
    """Marker Interface for IPlausibleUtilsView"""


@implementer(IPlausibleUtilsView)
class PlausibleUtilsView(BrowserView):

    def is_plausible_set(self):
        return True if get_plausible_vars() else False

    def add_link_user_action(self):
        return (
            True
            if api.portal.get_registry_record(
                name="collective.plausible.link_user_action"
            )
            else False
        )

    @property
    def get_plausible_instance_healthcheck(self):
        vars = get_plausible_vars()
        try:
            response = requests.get(f"https://{vars['plausible_url']}/api/health")
            return response.json()
        except:
            return False
