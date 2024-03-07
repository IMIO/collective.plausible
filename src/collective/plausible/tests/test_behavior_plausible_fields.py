# -*- coding: utf-8 -*-
from collective.plausible.behaviors.plausible_fields import IPlausibleFieldsMarker
from collective.plausible.utils import HAS_PLONE6
from collective.plausible.utils import get_plausible_infos
from collective.plausible.views.plausible_view import PlausibleView
from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING
from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import unittest


class PlausibleFieldsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]

        if HAS_PLONE6:
            # behavior already applied on Folder by profile
            # enabling it on Plone Site
            fti = queryUtility(IDexterityFTI, name="Plone Site")
            behaviors = list(fti.behaviors)
            behaviors.append("collective.plausible.plausible_fields")
            fti._updateProperty("behaviors", tuple(behaviors))

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

        if HAS_PLONE6:
            self.portal.plausible_enabled = True
            self.portal.plausible_url = "plonesite.plausible.be"
            self.portal.plausible_site = "plonesite.kamoulox.be"
            self.portal.plausible_token = "plonesitetoken123"
            self.portal.plausible_link_object_action = "True"
        self.snippet_plonesite = f'<script defer data-domain="plonesite.kamoulox.be" src="https://plonesite.plausible.be/js/script.js"></script>'
        self.iframe_plonesite = f'<iframe plausible-embed src="https://plonesite.plausible.be/share/plonesite.kamoulox.be?auth=plonesitetoken123&amp;embed=true&amp;theme=light&amp;background=transparent" scrolling="no" frameborder="0" loading="lazy" id="plausible" style="width: 1px; min-width: 100%; height: 1600px;">'

        self.portal["folder"].plausible_enabled = True
        self.portal["folder"].plausible_url = "folder.plausible.be"
        self.portal["folder"].plausible_site = "folder.kamoulox.be"
        self.portal["folder"].plausible_token = "foldertoken123"
        self.portal["folder"].plausible_link_object_action = "True"
        self.snippet_folder = f'<script defer data-domain="folder.kamoulox.be" src="https://folder.plausible.be/js/script.js"></script>'
        self.iframe_folder = f'<iframe plausible-embed src="https://folder.plausible.be/share/folder.kamoulox.be?auth=foldertoken123&amp;embed=true&amp;theme=light&amp;background=transparent" scrolling="no" frameborder="0" loading="lazy" id="plausible" style="width: 1px; min-width: 100%; height: 1600px;">'

        self.portal["folder2"].plausible_enabled = False
        self.portal["folder2"].plausible_url = "folder2.plausible.be"
        self.portal["folder2"].plausible_site = "folder2.kamoulox.be"
        self.portal["folder2"].plausible_token = "folder2token123"
        self.portal["folder2"].plausible_link_object_action = "True"
        self.iframe_folder2 = f'<iframe plausible-embed src="https://plonesite.plausible.be/share/plonesite.kamoulox.be?auth=plonesitetoken123&amp;embed=true&amp;theme=light&amp;background=transparent" scrolling="no" frameborder="0" loading="lazy" id="plausible" style="width: 1px; min-width: 100%; height: 1600px;">'

        self.portal["folder"]["subfolder"].plausible_enabled = True
        self.portal["folder"]["subfolder"].plausible_url = "subfolder.plausible.be"
        self.portal["folder"]["subfolder"].plausible_site = "subfolder.kamoulox.be"
        self.portal["folder"]["subfolder"].plausible_token = "subfoldertoken123"
        self.portal["folder"]["subfolder"].plausible_link_object_action = "True"
        self.snippet_subfolder = f'<script defer data-domain="subfolder.kamoulox.be" src="https://subfolder.plausible.be/js/script.js"></script>'
        self.iframe_subfolder = f'<iframe plausible-embed src="https://subfolder.plausible.be/share/subfolder.kamoulox.be?auth=subfoldertoken123&amp;embed=true&amp;theme=light&amp;background=transparent" scrolling="no" frameborder="0" loading="lazy" id="plausible" style="width: 1px; min-width: 100%; height: 1600px;">'

        self.portal["folder"]["subfolder2"].plausible_enabled = False
        self.portal["folder"]["subfolder2"].plausible_url = "subfolder2.plausible.be"
        self.portal["folder"]["subfolder2"].plausible_site = "subfolder2.kamoulox.be"
        self.iframe_subfolder2 = f'<iframe plausible-embed src="https://folder.plausible.be/share/folder.kamoulox.be?auth=foldertoken123&amp;embed=true&amp;theme=light&amp;background=transparent" scrolling="no" frameborder="0" loading="lazy" id="plausible" style="width: 1px; min-width: 100%; height: 1600px;">'

    def test_plausible_fields_testing_profile(self):
        self.assertFalse(IPlausibleFieldsMarker.providedBy(self.portal["document"]))
        self.assertTrue(IPlausibleFieldsMarker.providedBy(self.portal["folder"]))
        if HAS_PLONE6:
            self.assertTrue(IPlausibleFieldsMarker.providedBy(self.portal))

    def test_plausible_fields_behavior_fields(self):

        if HAS_PLONE6:
            # portal fields
            self.assertTrue(getattr(self.portal, "plausible_enabled", False))
            self.assertEqual(
                getattr(self.portal, "plausible_url"), "plonesite.plausible.be"
            )
            self.assertEqual(
                getattr(self.portal, "plausible_site"), "plonesite.kamoulox.be"
            )
            self.assertEqual(
                getattr(self.portal, "plausible_token"), "plonesitetoken123"
            )
            self.assertTrue(getattr(self.portal, "plausible_link_object_action", False))

        # folder fields
        self.assertTrue(getattr(self.portal["folder"], "plausible_enabled", False))
        self.assertEqual(
            getattr(self.portal["folder"], "plausible_url"), "folder.plausible.be"
        )
        self.assertEqual(
            getattr(self.portal["folder"], "plausible_site"), "folder.kamoulox.be"
        )
        self.assertEqual(
            getattr(self.portal["folder"], "plausible_token"), "foldertoken123"
        )
        self.assertTrue(
            getattr(self.portal["folder"], "plausible_link_object_action", False)
        )

        # subfolder fields
        self.assertTrue(
            getattr(self.portal["folder"]["subfolder"], "plausible_enabled", False)
        )
        self.assertEqual(
            getattr(self.portal["folder"]["subfolder"], "plausible_url"),
            "subfolder.plausible.be",
        )
        self.assertEqual(
            getattr(self.portal["folder"]["subfolder"], "plausible_site"),
            "subfolder.kamoulox.be",
        )
        self.assertEqual(
            getattr(self.portal["folder"]["subfolder"], "plausible_token"),
            "subfoldertoken123",
        )
        self.assertTrue(
            getattr(
                self.portal["folder"]["subfolder"],
                "plausible_link_object_action",
                False,
            )
        )

        # subfolder2 fields
        self.assertFalse(
            getattr(self.portal["folder"]["subfolder2"], "plausible_enabled", False)
        )
        self.assertEqual(
            getattr(self.portal["folder"]["subfolder2"], "plausible_url"),
            "subfolder2.plausible.be",
        )
        self.assertEqual(
            getattr(self.portal["folder"]["subfolder2"], "plausible_site"),
            "subfolder2.kamoulox.be",
        )
        self.assertFalse(
            getattr(
                self.portal["folder"]["subfolder2"],
                "plausible_link_object_action",
                False,
            )
        )

    def test_plausible_fields_behavior_traversing(self):

        if HAS_PLONE6:
            self.assertIn(self.snippet_plonesite, self.portal())

        uid = self.portal["folder"].UID()
        folder = api.content.get(UID=uid)
        self.assertIn(self.snippet_folder, folder())

        uid = self.portal["folder"]["subfolder"].UID()
        subfolder = api.content.get(UID=uid)
        self.assertIn(self.snippet_subfolder, subfolder())

        uid = self.portal["folder"]["subfolder"]["document"].UID()
        document_in_subfolder = api.content.get(UID=uid)
        self.assertIn(self.snippet_subfolder, document_in_subfolder())

        uid = self.portal["folder"]["subfolder2"].UID()
        subfolder2 = api.content.get(UID=uid)
        self.assertIn(self.snippet_folder, subfolder2())

        uid = self.portal["folder"]["subfolder2"]["document"].UID()
        document_in_subfolder2 = api.content.get(UID=uid)
        self.assertIn(self.snippet_folder, document_in_subfolder2())

        uid = self.portal["folder"]["document"].UID()
        document_in_folder = api.content.get(UID=uid)
        self.assertIn(self.snippet_folder, document_in_folder())

        uid = self.portal["folder2"]["document"].UID()
        document_in_folder2 = api.content.get(UID=uid)
        if HAS_PLONE6:
            self.assertIn(self.snippet_plonesite, document_in_folder2())
        else:
            self.assertNotIn(self.snippet_plonesite, document_in_folder2())

        uid = self.portal["folder2"]["subfolder"].UID()
        subfolder = api.content.get(UID=uid)
        if HAS_PLONE6:
            self.assertIn(self.snippet_plonesite, subfolder())
        else:
            self.assertNotIn(self.snippet_plonesite, subfolder())

        if HAS_PLONE6:
            # disabling behavior on plone site
            fti = queryUtility(IDexterityFTI, name="Plone Site")
            behaviors = list(fti.behaviors)
            behaviors.remove("collective.plausible.plausible_fields")
            fti._updateProperty("behaviors", tuple(behaviors))
            for property in [
                "plausible_enabled",
                "plausible_url",
                "plausible_site",
                "plausible_token",
                "plausible_link_object_action",
            ]:
                setattr(self.portal, property, None)
            for snippet in [
                self.snippet_plonesite,
                self.snippet_folder,
                self.snippet_subfolder,
            ]:
                self.assertNotIn(snippet, self.portal())

        uid = self.portal["folder2"]["subfolder"].UID()
        subfolder = api.content.get(UID=uid)
        self.assertNotIn(self.snippet_plonesite, subfolder())

    def test_plausible_view_traversing(self):
        view_plonesite = PlausibleView(self.portal, self.request)
        view_folder = PlausibleView(self.portal["folder"], self.request)
        view_subfolder = PlausibleView(self.portal["folder"]["subfolder"], self.request)
        view_subfolder2 = PlausibleView(
            self.portal["folder"]["subfolder2"], self.request
        )
        view_folder2 = PlausibleView(self.portal["folder2"], self.request)
        view_subfolder3 = PlausibleView(
            self.portal["folder2"]["subfolder"], self.request
        )
        if HAS_PLONE6:
            self.assertIn(self.iframe_plonesite, view_plonesite())
        self.assertIn(self.iframe_folder, view_folder())
        self.assertIn(self.iframe_subfolder, view_subfolder())
        self.assertIn(self.iframe_folder, view_subfolder2())
        if HAS_PLONE6:
            self.assertIn(self.iframe_plonesite, view_folder2())
            self.assertIn(self.iframe_plonesite, view_subfolder3())
        else:
            self.assertNotIn(self.iframe_plonesite, view_folder2())
            self.assertNotIn(self.iframe_plonesite, view_subfolder3())

    def test_plausible_object_action(self):

        if HAS_PLONE6:
            self.assertTrue(
                get_plausible_infos(self.portal)["plausible_link_object_action"]
            )

        self.assertTrue(
            get_plausible_infos(self.portal["folder"])["plausible_link_object_action"]
        )

        self.assertTrue(
            get_plausible_infos(self.portal["folder"]["subfolder"])[
                "plausible_link_object_action"
            ]
        )

        self.assertTrue(
            get_plausible_infos(self.portal["folder"]["subfolder2"])[
                "plausible_link_object_action"
            ]
        )

        if HAS_PLONE6:
            self.assertTrue(
                get_plausible_infos(self.portal["folder2"])[
                    "plausible_link_object_action"
                ]
            )
            self.assertTrue(
                get_plausible_infos(self.portal["folder2"]["subfolder"])[
                    "plausible_link_object_action"
                ]
            )
        else:
            self.assertFalse(
                get_plausible_infos(self.portal["folder2"])[
                    "plausible_link_object_action"
                ]
            )
            self.assertFalse(
                get_plausible_infos(self.portal["folder2"]["subfolder"])[
                    "plausible_link_object_action"
                ]
            )

        if HAS_PLONE6:
            # disabling behavior on plone site
            fti = queryUtility(IDexterityFTI, name="Plone Site")
            behaviors = list(fti.behaviors)
            behaviors.remove("collective.plausible.plausible_fields")
            fti._updateProperty("behaviors", tuple(behaviors))
            for property in [
                "plausible_enabled",
                "plausible_url",
                "plausible_site",
                "plausible_token",
                "plausible_link_object_action",
            ]:
                setattr(self.portal, property, None)

        if HAS_PLONE6:
            self.assertFalse(
                get_plausible_infos(self.portal)["plausible_link_object_action"]
            )

        self.assertTrue(
            get_plausible_infos(self.portal["folder"])["plausible_link_object_action"]
        )

        self.assertFalse(
            get_plausible_infos(self.portal["folder2"]["subfolder"])[
                "plausible_link_object_action"
            ]
        )


class PlausibleFieldsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
