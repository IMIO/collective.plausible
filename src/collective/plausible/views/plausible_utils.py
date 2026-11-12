from collective.plausible.utils import get_plausible_infos
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IPlausibleUtilsView(Interface):
    """Marker Interface for IPlausibleUtilsView"""


@implementer(IPlausibleUtilsView)
class PlausibleUtilsView(BrowserView):

    def is_plausible_set(self):
        plausible_infos = get_plausible_infos(self)
        for key in plausible_infos:
            if plausible_infos[key] == "" or not plausible_infos[key]:
                return False
        return True

    def add_link_object_action(self):
        return get_plausible_infos(self).get("plausible_link_object_action", False)

    def show_link_object_action(self):
        return self.add_link_object_action() and self.is_plausible_set()
