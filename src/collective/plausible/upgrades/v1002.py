# -*- coding: utf-8 -*-

from . import logger
from .base import reload_gs_profile
from collective.plausible import _
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def upgrade(setup_tool=None):
    """ """
    logger.info("Running upgrade (Python): Replace action linking to @@plausible-view")
    registry = getUtility(IRegistry)
    if "collective.plausible.link_user_action" in registry.records:
        del registry.records["collective.plausible.link_user_action"]
    reload_gs_profile(setup_tool)
