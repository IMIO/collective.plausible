# -*- coding: utf-8 -*-

from plone import api

import os
from collective.plausible.behaviors.plausible_fields import IPlausibleFieldsMarker
from pkg_resources import parse_version
from plone.api import env
from Products.CMFPlone.Portal import PloneSite
from Products.CMFPlone.utils import parent


HAS_PLONE6 = parse_version(env.plone_version()) >= parse_version("6.0")


def get_plausible_infos(content):

    while (not isinstance(content, PloneSite)) and not (
        IPlausibleFieldsMarker.providedBy(content)
        and getattr(content, "plausible_enabled", False)
    ):
        content = parent(content)
    # __import__("pdb").set_trace()
    return {
        "plausible_enabled": getattr(content, "plausible_enabled", False),
        "plausible_url": getattr(content, "plausible_url", ""),
        "plausible_site": getattr(content, "plausible_site", ""),
        "plausible_token": getattr(content, "plausible_token", ""),
        "plausible_link_object_action": getattr(
            content, "plausible_link_object_action", False
        ),
    }
