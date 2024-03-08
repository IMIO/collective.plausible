# -*- coding: utf-8 -*-

from collective.plausible.utils import get_plausible_infos
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope.interface import Interface
import requests


class IPlausibleHealthcheckView(Interface):
    """Marker Interface for IPlausibleHealthcheckView"""


@implementer(IPlausibleHealthcheckView)
class PlausibleHealthcheckView(BrowserView):
    index = ViewPageTemplateFile("plausible_healthcheck.pt")

    def __call__(self):
        self.vars = get_plausible_infos(self)
        return self.index()

    @property
    def is_plausible_set(self):
        return True if get_plausible_infos(self) else False

    @property
    def get_plausible_instance_healthcheck(self):
        vars = get_plausible_infos(self)
        try:
            response = requests.get(
                f"https://{vars.get('plausible_url', '')}/api/health"
            )
            return response.json()
        except:
            return False
