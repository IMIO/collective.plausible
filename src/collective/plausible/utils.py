from collective.plausible.behaviors.plausible_fields import IPlausibleFieldsMarker
from Products.CMFPlone.Portal import PloneSite
from Products.CMFPlone.utils import parent


def get_plausible_infos(content):

    while (not isinstance(content, PloneSite)) and not (
        IPlausibleFieldsMarker.providedBy(content)
        and getattr(content, "plausible_enabled", False)
    ):
        content = parent(content)
    return {
        "plausible_enabled": getattr(content, "plausible_enabled", False),
        "plausible_url": getattr(content, "plausible_url", ""),
        "plausible_site": getattr(content, "plausible_site", ""),
        "plausible_token": getattr(content, "plausible_token", ""),
        "plausible_link_object_action": getattr(
            content, "plausible_link_object_action", False
        ),
    }


def is_plausible_set(infos):
    """Plausible is enabled and its server and site are filled in."""
    return bool(
        infos["plausible_enabled"]
        and infos["plausible_url"]
        and infos["plausible_site"]
    )
