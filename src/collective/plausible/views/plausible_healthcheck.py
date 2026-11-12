from collective.plausible.utils import get_plausible_infos
from collective.plausible.utils import is_plausible_set
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope.interface import Interface

import requests

HEALTHCHECK_TIMEOUT = 5  # seconds


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
        return is_plausible_set(get_plausible_infos(self))

    @property
    def get_plausible_instance_healthcheck(self):
        vars = get_plausible_infos(self)
        try:
            response = requests.get(
                f"https://{vars.get('plausible_url', '')}/api/health",
                timeout=HEALTHCHECK_TIMEOUT,
            )
            return response.json()
        except Exception:
            return False
