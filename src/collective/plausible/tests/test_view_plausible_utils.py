from collective.plausible.testing import COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING
from collective.plausible.views.plausible_utils import PlausibleUtilsView
from collective.plausible.views.plausible_view import PlausibleView
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import unittest


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        # behavior already applied on Folder by profile
        # enabling it on Plone Site
        fti = queryUtility(IDexterityFTI, name="Plone Site")
        behaviors = list(fti.behaviors)
        behaviors.append("collective.plausible.plausible_fields")
        fti._updateProperty("behaviors", tuple(behaviors))

    def test_add_link_object_action(self):
        utils_view = PlausibleUtilsView(self.portal, self.request)
        self.assertFalse(utils_view.add_link_object_action())
        self.portal.plausible_link_object_action = True
        self.assertTrue(utils_view.add_link_object_action())

    def test_is_plausible_set(self):
        utils_view = PlausibleUtilsView(self.portal, self.request)
        self.assertFalse(utils_view.is_plausible_set())

        self.portal.plausible_enabled = True
        self.portal.plausible_url = "plonesite.plausible.be"
        self.portal.plausible_site = "plonesite.kamoulox.be"
        self.portal.plausible_token = ""
        self.assertTrue(utils_view.is_plausible_set())

        for field, empty in (
            ("plausible_url", ""),
            ("plausible_site", ""),
            ("plausible_enabled", False),
        ):
            value = getattr(self.portal, field)
            setattr(self.portal, field, empty)
            self.assertFalse(utils_view.is_plausible_set(), field)
            setattr(self.portal, field, value)

    def test_plausible_view_not_set(self):
        view = PlausibleView(self.portal, self.request)
        self.assertFalse(view.is_plausible_set)
        page = view()
        self.assertIn("Plausible analytics is not set", page)
        self.assertNotIn("<iframe", page)
