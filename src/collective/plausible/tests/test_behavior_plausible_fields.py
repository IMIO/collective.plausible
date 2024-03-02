# -*- coding: utf-8 -*-
from collective.plausible.behaviors.plausible_fields import IPlausibleFieldsMarker
from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING
from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
import unittest


class PlausibleFieldsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        applyProfile(self.portal, "collective.plausible:testing")
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Document", "document")
        api.content.create(self.portal, "Folder", "folder")
        api.content.create(self.portal, "Folder", "folder2")
        api.content.create(self.portal["folder"], "Folder", "subfolder")
        api.content.create(self.portal["folder"], "Folder", "subfolder2")
        api.content.create(self.portal["folder"], "Document", "document")
        api.content.create(self.portal["folder"]["subfolder"], "Document", "document")
        api.content.create(self.portal["folder"]["subfolder2"], "Document", "document")
        api.content.create(self.portal["folder2"], "Document", "document")
        api.content.create(self.portal["folder2"], "Folder", "subfolder")

    def test_plausible_fields_testing_profile(self):
        self.assertFalse(IPlausibleFieldsMarker.providedBy(self.portal["document"]))
        self.assertTrue(IPlausibleFieldsMarker.providedBy(self.portal["folder"]))
        # TODO
        # self.assertTrue(IPlausibleFieldsMarker.providedBy(self.portal))

    def test_plausible_fields_behavior(self):
        self.portal.plausible_enabled = True
        self.portal.plausible_url = "plonesite.plausible.be"
        self.portal.plausible_site = "plonesite.kamoulox.be"
        self.portal.plausible_token = "plonesitetoken123"
        self.portal.plausible_link_object_action = "True"
        snippet_plonesite = f'<script defer data-domain="plonesite.kamoulox.be" src="https://plonesite.plausible.be/js/script.js"></script>'

        self.portal["folder"].plausible_enabled = True
        self.portal["folder"].plausible_url = "folder.plausible.be"
        self.portal["folder"].plausible_site = "folder.kamoulox.be"
        self.portal["folder"].plausible_token = "foldertoken123"
        self.portal["folder"].plausible_link_object_action = "True"
        snippet_folder = f'<script defer data-domain="folder.kamoulox.be" src="https://folder.plausible.be/js/script.js"></script>'

        self.portal["folder"].plausible_enabled = True
        self.portal["folder"].plausible_url = "folder.plausible.be"
        self.portal["folder"].plausible_site = "folder.kamoulox.be"
        self.portal["folder"].plausible_token = "foldertoken123"
        self.portal["folder"].plausible_link_object_action = "True"
        snippet_folder = f'<script defer data-domain="folder.kamoulox.be" src="https://folder.plausible.be/js/script.js"></script>'

        self.portal["folder2"].plausible_enabled = False
        self.portal["folder2"].plausible_url = "folder2.plausible.be"
        self.portal["folder2"].plausible_site = "folder2.kamoulox.be"
        self.portal["folder2"].plausible_token = "folder2token123"
        self.portal["folder2"].plausible_link_object_action = "True"

        self.portal["folder"]["subfolder"].plausible_enabled = True
        self.portal["folder"]["subfolder"].plausible_url = "subfolder.plausible.be"
        self.portal["folder"]["subfolder"].plausible_site = "subfolder.kamoulox.be"
        self.portal["folder"]["subfolder"].plausible_token = "subfoldertoken123"
        self.portal["folder"]["subfolder"].plausible_link_object_action = "True"
        snippet_subfolder = f'<script defer data-domain="subfolder.kamoulox.be" src="https://subfolder.plausible.be/js/script.js"></script>'

        self.portal["folder"]["subfolder2"].plausible_enabled = False
        self.portal["folder"]["subfolder2"].plausible_url = "subfolder2.plausible.be"
        self.portal["folder"]["subfolder2"].plausible_site = "subfolder2.kamoulox.be"

        self.assertIn(snippet_plonesite, self.portal())

        uid = self.portal["folder"].UID()
        folder = api.content.get(UID=uid)
        self.assertIn(snippet_folder, folder())

        uid = self.portal["folder"]["subfolder"].UID()
        subfolder = api.content.get(UID=uid)
        self.assertIn(snippet_subfolder, subfolder())

        uid = self.portal["folder"]["subfolder"]["document"].UID()
        document_in_subfolder = api.content.get(UID=uid)
        self.assertIn(snippet_subfolder, document_in_subfolder())

        uid = self.portal["folder"]["subfolder2"].UID()
        subfolder2 = api.content.get(UID=uid)
        self.assertIn(snippet_folder, subfolder2())

        uid = self.portal["folder"]["subfolder2"]["document"].UID()
        document_in_subfolder2 = api.content.get(UID=uid)
        self.assertIn(snippet_folder, document_in_subfolder2())

        uid = self.portal["folder"]["document"].UID()
        document_in_folder = api.content.get(UID=uid)
        self.assertIn(snippet_folder, document_in_folder())

        uid = self.portal["folder2"]["document"].UID()
        document_in_folder2 = api.content.get(UID=uid)
        self.assertIn(snippet_plonesite, document_in_folder2())

        uid = self.portal["folder2"]["subfolder"].UID()
        subfolder = api.content.get(UID=uid)
        self.assertIn(snippet_plonesite, subfolder())


class PlausibleFieldsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
