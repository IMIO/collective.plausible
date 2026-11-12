from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING
from collective.plausible.views.plausible_healthcheck import PlausibleHealthcheckView
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest import mock

import requests
import unittest


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Folder", "folder")
        self.portal["folder"].plausible_enabled = True
        self.portal["folder"].plausible_url = "folder.plausible.be"
        self.portal["folder"].plausible_site = "folder.kamoulox.be"
        self.portal["folder"].plausible_token = "foldertoken123"
        self.portal["folder"].plausible_link_object_action = "True"

    @mock.patch("requests.get")
    def test_get_plausible_instance_healthcheck_success(self, mock_get):
        healthcheck_view = PlausibleHealthcheckView(self.portal["folder"], self.request)
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "clickhouse": "ok",
            "postgres": "ok",
            "sites_cache": "ok",
        }
        mock_get.return_value = mock_response
        result = healthcheck_view.get_plausible_instance_healthcheck

        self.assertEqual(
            result,
            {
                "clickhouse": "ok",
                "postgres": "ok",
                "sites_cache": "ok",
            },
        )
        mock_get.assert_called_once_with(
            "https://folder.plausible.be/api/health", timeout=5
        )

    @mock.patch("requests.get")
    def test_get_plausible_instance_healthcheck_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException
        healthcheck_view = PlausibleHealthcheckView(self.portal["folder"], self.request)
        result = healthcheck_view.get_plausible_instance_healthcheck
        self.assertFalse(result)
        mock_get.assert_called_once_with(
            "https://folder.plausible.be/api/health", timeout=5
        )

    def test_healthcheck_is_plausible_set(self):
        healthcheck_view = PlausibleHealthcheckView(self.portal["folder"], self.request)
        self.assertTrue(healthcheck_view.is_plausible_set)

    @mock.patch("requests.get")
    def test_healthcheck_index(self, mock_get):
        mock_get.return_value.json.return_value = {
            "clickhouse": "ch-ok",
            "postgres": "pg-ok",
            "sites_cache": "sc-ok",
        }
        healthcheck_view = PlausibleHealthcheckView(self.portal["folder"], self.request)
        page = healthcheck_view()
        self.assertIn("<span >Plausible server healthcheck</span>", page)
        for status in ("ch-ok", "pg-ok", "sc-ok"):
            self.assertIn(status, page)
        mock_get.assert_called_once()

    @mock.patch("requests.get")
    def test_healthcheck_index_not_set(self, mock_get):
        healthcheck_view = PlausibleHealthcheckView(self.portal, self.request)
        self.assertFalse(healthcheck_view.is_plausible_set)
        self.assertIn("Plausible fields are not set yet", healthcheck_view())
        mock_get.assert_not_called()
