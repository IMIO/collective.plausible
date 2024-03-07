# -*- coding: utf-8 -*-
from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING
from collective.plausible.views.plausible_utils import PlausibleUtilsView
from collective.plausible.utils import HAS_PLONE6
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest import mock
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import os
import requests
import unittest


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        if not HAS_PLONE6:
            return
        # behavior already applied on Folder by profile
        # enabling it on Plone Site
        fti = queryUtility(IDexterityFTI, name="Plone Site")
        behaviors = list(fti.behaviors)
        behaviors.append("collective.plausible.plausible_fields")
        fti._updateProperty("behaviors", tuple(behaviors))

    @mock.patch("requests.get")
    def test_get_plausible_instance_healthcheck_success(self, mock_get):
        utils_view = PlausibleUtilsView(self.portal, self.request)
        self.portal.plausible_url = "plausible-url"
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "clickhouse": "ok",
            "postgres": "ok",
            "sites_cache": "ok",
        }
        mock_get.return_value = mock_response
        result = utils_view.get_plausible_instance_healthcheck

        self.assertEqual(
            result,
            {
                "clickhouse": "ok",
                "postgres": "ok",
                "sites_cache": "ok",
            },
        )
        mock_get.assert_called_once_with("https://plausible-url/api/health")

    @mock.patch("requests.get")
    def test_get_plausible_instance_healthcheck_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException
        utils_view = PlausibleUtilsView(self.portal, self.request)
        self.portal.plausible_url = "plausible-url"
        result = utils_view.get_plausible_instance_healthcheck
        self.assertFalse(result)
        mock_get.assert_called_once_with("https://plausible-url/api/health")

    def test_add_link_object_action(self):
        utils_view = PlausibleUtilsView(self.portal, self.request)
        self.assertFalse(utils_view.add_link_object_action())
        self.portal.plausible_link_object_action = True
        self.assertTrue(utils_view.add_link_object_action())

    def test_is_plausible_set(self):
        utils_view = PlausibleUtilsView(self.portal, self.request)
        self.assertFalse(utils_view.is_plausible_set())
