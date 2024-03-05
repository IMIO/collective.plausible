# -*- coding: utf-8 -*-
from collective.plausible.interfaces import ICollectivePlausibleLayer
from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING
from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.Five.browser import BrowserView
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import unittest


class ViewletIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.app = self.layer["app"]
        self.request = self.app.REQUEST
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Document", "other-document")
        api.content.create(self.portal, "News Item", "newsitem")

    def test_plausible_snippet_viewlet_is_registered(self):
        view = BrowserView(self.portal["other-document"], self.request)
        manager_name = "plone.portalfooter"
        alsoProvides(self.request, ICollectivePlausibleLayer)
        manager = queryMultiAdapter(
            (self.portal["other-document"], self.request, view),
            IViewletManager,
            manager_name,
            default=None,
        )
        self.assertIsNotNone(manager)
        manager.update()
        my_viewlet = [
            v for v in manager.viewlets if v.__name__ == "plausible-snippet-viewlet"
        ]  # NOQA: E501
        self.assertEqual(len(my_viewlet), 1)


class ViewletFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
