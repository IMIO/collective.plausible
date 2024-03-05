# -*- coding: utf-8 -*-

from collective.plausible import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


class IPlausibleFieldsMarker(Interface):
    pass


@provider(IFormFieldProvider)
class IPlausibleFields(model.Schema):
    """ """

    directives.fieldset(
        "plausible_fields",
        label=_("Plausible fields"),
        description=_("Plausible analytics fields"),
        fields=[
            "plausible_enabled",
            "plausible_url",
            "plausible_site",
            "plausible_token",
            "plausible_link_object_action",
        ],
    )

    plausible_enabled = schema.Bool(
        title=_("Enable Plausible"),
        description=_(
            "Enable Plausible analytics tracking on this content and all its children."
        ),
        default=False,
        required=False,
        readonly=False,
    )

    plausible_url = schema.TextLine(
        title=_("Plausible URL"),
        description=_("Example : plausible.imio.be"),
        default="",
        required=False,
        readonly=False,
    )

    plausible_site = schema.TextLine(
        title=_("Plausible Site"),
        description=_("Example : imio.be"),
        default="",
        required=False,
        readonly=False,
    )

    plausible_token = schema.TextLine(
        title=_("Plausible token"),
        description=_("Plausible authentification token"),
        default="",
        required=False,
        readonly=False,
    )

    plausible_link_object_action = schema.Bool(
        title=_("Add a link in the object menu"),
        description=_("Add a link to the statistics browser view in the object menu"),
        default=False,
        required=False,
        readonly=False,
    )


@implementer(IPlausibleFields)
@adapter(IPlausibleFieldsMarker)
class PlausibleFields(object):  # pragma: no cover
    def __init__(self, context):
        self.context = context

    @property
    def plausible_enabled(self):
        if safe_hasattr(self.context, "plausible_enabled"):
            return self.context.plausible_enabled
        return None

    @plausible_enabled.setter
    def plausible_enabled(self, value):
        self.context.plausible_enabled = value

    @property
    def plausible_url(self):
        if safe_hasattr(self.context, "plausible_url"):
            return self.context.plausible_url
        return None

    @plausible_url.setter
    def plausible_url(self, value):
        self.context.plausible_url = value

    @property
    def plausible_site(self):
        if safe_hasattr(self.context, "plausible_site"):
            return self.context.plausible_site
        return None

    @plausible_site.setter
    def plausible_site(self, value):
        self.context.plausible_site = value

    @property
    def plausible_token(self):
        if safe_hasattr(self.context, "plausible_token"):
            return self.context.plausible_token
        return None

    @plausible_token.setter
    def plausible_token(self, value):
        self.context.plausible_token = value

    @property
    def plausible_link_object_action(self):
        if safe_hasattr(self.context, "plausible_link_object_action"):
            return self.context.plausible_link_object_action
        return None

    @plausible_link_object_action.setter
    def plausible_link_object_action(self, value):
        self.context.plausible_link_object_action = value
