# -*- coding: utf-8 -*-

from collective.plausible.behaviors.plausible_fields import IPlausibleFieldsMarker
from plone.app.layout.viewlets import ViewletBase
from Products.CMFPlone.Portal import PloneSite
from Products.CMFPlone.utils import parent


class PlausibleSnippetViewlet(ViewletBase):

    def update(self):
        self.plausible_infos = self.get_plausible_infos()
        self.plausible_url = self.get_plausible_url()
        self.plausible_site = self.get_plausible_site()
        self.is_plausible_set = self.get_is_plausible_set()
        self.is_plausible_enabled = self.get_is_plausible_enabled()

    def get_plausible_infos(self):
        while (
            not IPlausibleFieldsMarker.providedBy(self)
            or not getattr(self, "plausible_enabled", False)
        ) and not isinstance(self, PloneSite):
            self = parent(self)
        return {
            "plausible_enabled": getattr(self, "plausible_enabled", False),
            "plausible_url": getattr(self, "plausible_url", ""),
            "plausible_site": getattr(self, "plausible_site", ""),
        }

    def get_is_plausible_set(self):
        return True if self.get_plausible_infos() else False

    def get_is_plausible_enabled(self):
        return self.plausible_infos["plausible_enabled"]

    def get_plausible_url(self):
        return self.plausible_infos["plausible_url"]

    def get_plausible_site(self):
        return self.plausible_infos["plausible_site"]

    def index(self):
        return super(PlausibleSnippetViewlet, self).render()
