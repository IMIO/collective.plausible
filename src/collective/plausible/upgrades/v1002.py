# -*- coding: utf-8 -*-

from . import logger
from .base import reload_gs_profile
from collective.plausible import _
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def upgrade(setup_tool=None):
    """ """
    logger.info("Running upgrade (Python): Replace action linking to @@plausible-view")
    registry = getUtility(IRegistry)
    if "collective.plausible.link_user_action" in registry.records:
        del registry.records["collective.plausible.link_user_action"]
    if "collective.plausible.url" in registry.records:
        del registry.records["collective.plausible.url"]
    if "collective.plausible.site" in registry.records:
        del registry.records["collective.plausible.site"]
    if "collective.plausible.token" in registry.records:
        del registry.records["collective.plausible.token"]
    reload_gs_profile(setup_tool)
