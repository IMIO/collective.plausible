# -*- coding: utf-8 -*-

from plone import api

import os
from collective.plausible.behaviors.plausible_fields import IPlausibleFieldsMarker
from Products.CMFPlone.Portal import PloneSite
from Products.CMFPlone.utils import parent


def get_plausible_infos(content):
    while (
        not IPlausibleFieldsMarker.providedBy(content)
        or not getattr(content, "plausible_enabled", False)
    ) and not isinstance(content, PloneSite):
        content = parent(content)
    return {
        "plausible_enabled": getattr(content, "plausible_enabled", False),
        "plausible_url": getattr(content, "plausible_url", ""),
        "plausible_site": getattr(content, "plausible_site", ""),
        "plausible_token": getattr(content, "plausible_token", ""),
    }


def get_plausible_vars():
    env_plausible_url = os.getenv("COLLECTIVE_PLAUSIBLE_URL", "")
    env_plausible_site = os.getenv("COLLECTIVE_PLAUSIBLE_SITE", "")
    env_plausible_token = os.getenv("COLLECTIVE_PLAUSIBLE_TOKEN", "")

    plausible_url = (
        env_plausible_url
        if (env_plausible_url and env_plausible_url != "")
        else api.portal.get_registry_record("collective.plausible.url")
    )
    plausible_site = (
        env_plausible_site
        if (env_plausible_site and env_plausible_site != "")
        else api.portal.get_registry_record("collective.plausible.site")
    )
    plausible_token = (
        env_plausible_token
        if (env_plausible_token and env_plausible_token != "")
        else api.portal.get_registry_record("collective.plausible.token")
    )
    if all([plausible_site, plausible_url, plausible_token]):
        plausible_vars = {
            "plausible_url": plausible_url,
            "plausible_site": plausible_site,
            "plausible_token": plausible_token,
        }
        return plausible_vars
    else:
        return None
