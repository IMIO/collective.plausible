# -*- coding: utf-8 -*-
from collective.plausible.views.plausible_utils import PlausibleUtilsView
from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest import mock
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import os
import requests
import unittest


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    @mock.patch("requests.get")
    @mock.patch.dict(
        os.environ,
        {
            "COLLECTIVE_PLAUSIBLE_SITE": "kamoulox.be",
            "COLLECTIVE_PLAUSIBLE_TOKEN": "abc",
            "COLLECTIVE_PLAUSIBLE_URL": "plausible-url",
        },
    )
    def test_get_plausible_instance_healthcheck_success(self, mock_get):
        utils = PlausibleUtilsView(self.portal, self.request)
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "clickhouse": "ok",
            "postgres": "ok",
            "sites_cache": "ok",
        }
        mock_get.return_value = mock_response
        result = utils.get_plausible_instance_healthcheck

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
    @mock.patch.dict(
        os.environ,
        {
            "COLLECTIVE_PLAUSIBLE_SITE": "kamoulox.be",
            "COLLECTIVE_PLAUSIBLE_TOKEN": "abc",
            "COLLECTIVE_PLAUSIBLE_URL": "plausible-url",
        },
    )
    def test_get_plausible_instance_healthcheck_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException
        utils = PlausibleUtilsView(self.portal, self.request)
        result = utils.get_plausible_instance_healthcheck
        self.assertFalse(result)
        mock_get.assert_called_once_with("https://plausible-url/api/health")

    def test_add_link_user_action(self):
        utils = PlausibleUtilsView(self.portal, self.request)
        with mock.patch(
            "plone.api.portal.get_registry_record"
        ) as mock_get_registry_record:
            mock_get_registry_record.return_value = True
            result = utils.add_link_user_action()

            self.assertTrue(result)
            mock_get_registry_record.assert_called_once_with(
                name="collective.plausible.link_user_action"
            )

            mock_get_registry_record.return_value = False
            result = utils.add_link_user_action()
            self.assertFalse(result)
            mock_get_registry_record.assert_called_with(
                name="collective.plausible.link_user_action"
            )

    @mock.patch("collective.plausible.views.plausible_utils.get_plausible_vars")
    def test_is_plausible_set_true(self, mock_get_plausible_vars):
        mock_get_plausible_vars.return_value = {
            "plausible_url": "plausibleurl.be",
            "plausible_site": "plausiblesite.be",
            "plausible_token": "plausibletoken",
        }
        utils = PlausibleUtilsView(self.portal, self.request)
        result = utils.is_plausible_set()
        self.assertTrue(result)
        mock_get_plausible_vars.assert_called_once()

    @mock.patch("collective.plausible.views.plausible_utils.get_plausible_vars")
    def test_is_plausible_set_false(self, mock_get_plausible_vars):
        mock_get_plausible_vars.return_value = None
        utils = PlausibleUtilsView(self.portal, self.request)
        result = utils.is_plausible_set()
        self.assertFalse(result)
        mock_get_plausible_vars.assert_called_once()
