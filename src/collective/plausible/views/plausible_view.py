# -*- coding: utf-8 -*-

from collective.plausible.utils import get_plausible_infos
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope.interface import Interface


class IPlausibleView(Interface):
    """Marker Interface for IPlausibleView"""


@implementer(IPlausibleView)
class PlausibleView(BrowserView):
    index = ViewPageTemplateFile("plausible_view.pt")

    def __call__(self):
        self.vars = get_plausible_infos(self)
        return self.index()

    @property
    def is_plausible_set(self):
        return True if get_plausible_infos(self) else False

    @property
    def get_embedhostjs_src(self):
        return f"https://{self.vars['plausible_url']}/js/embed.host.js"

    @property
    def get_iframe_src(self):
        return f"https://{self.vars['plausible_url']}/share/{self.vars['plausible_site']}?auth={self.vars['plausible_token']}&embed=true&theme=light&background=transparent"
