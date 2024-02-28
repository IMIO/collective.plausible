# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase


class PlausibleSnippetViewlet(ViewletBase):

    def update(self):
        self.plausible_url = self.get_plausible_url()
        self.plausible_site = self.get_plausible_site()

    def get_plausible_url(self):
        # fmt: off
        # import pdb; pdb.set_trace()
        # fmt: on
        return self.context.url

    def get_plausible_site(self):
        return self.context.site

    def index(self):
        return super(PlausibleSnippetViewlet, self).render()
