# -*- coding: utf-8 -*-
from collective.plausible.behaviors.plausible_fields import IPlausibleFieldsMarker
from collective.plausible.testing import (  # noqa
    COLLECTIVE_PLAUSIBLE_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class PlausibleFieldsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_plausible_fields(self):
        behavior = getUtility(IBehavior, "collective.plausible.plausible_fields")
        self.assertEqual(
            behavior.marker,
            IPlausibleFieldsMarker,
        )
