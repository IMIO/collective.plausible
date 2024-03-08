# -*- coding: utf-8 -*-

from collective.plausible.utils import get_plausible_infos
from plone.app.layout.viewlets import ViewletBase


class PlausibleSnippetViewlet(ViewletBase):

    def update(self):
        self.plausible_infos = get_plausible_infos(self)
        self.plausible_url = self.get_plausible_url()
        self.plausible_site = self.get_plausible_site()
        self.is_plausible_set = self.get_is_plausible_set()
        self.is_plausible_enabled = self.get_is_plausible_enabled()

    def get_is_plausible_set(self):
        return True if get_plausible_infos(self) else False

    def get_is_plausible_enabled(self):
        return self.plausible_infos["plausible_enabled"]

    def get_plausible_url(self):
        return self.plausible_infos["plausible_url"]

    def get_plausible_site(self):
        return self.plausible_infos["plausible_site"]

    def index(self):  # pragma: no cover
        return super(PlausibleSnippetViewlet, self).render()
