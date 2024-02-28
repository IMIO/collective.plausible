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
        fields=["url", "site", "token", "link_user_action"],
    )

    url = schema.TextLine(
        title=_("Plausible URL"),
        description=_("Example : plausible.imio.be"),
        default="",
        required=False,
        readonly=False,
    )

    site = schema.TextLine(
        title=_("Plausible Site"),
        description=_("Example : imio.be"),
        default="",
        required=False,
        readonly=False,
    )

    token = schema.TextLine(
        title=_("Plausible token"),
        description=_("Plausible authentification token"),
        default="",
        required=False,
        readonly=False,
    )

    link_user_action = schema.Bool(
        title=_("Add a link in the user menu"),
        description=_("Add a link to the statistics browser view in the user menu"),
        default=True,
        required=False,
        readonly=False,
    )


@implementer(IPlausibleFields)
@adapter(IPlausibleFieldsMarker)
class PlausibleFields(object):
    def __init__(self, context):
        self.context = context

    @property
    def url(self):
        if safe_hasattr(self.context, "url"):
            return self.context.url
        return None

    @url.setter
    def url(self, value):
        self.context.url = value

    @property
    def site(self):
        if safe_hasattr(self.context, "site"):
            return self.context.site
        return None

    @site.setter
    def site(self, value):
        self.context.site = value

    @property
    def token(self):
        if safe_hasattr(self.context, "token"):
            return self.context.token
        return None

    @token.setter
    def token(self, value):
        self.context.token = value

    @property
    def link_user_action(self):
        if safe_hasattr(self.context, "link_user_action"):
            return self.context.link_user_action
        return None

    @link_user_action.setter
    def link_user_action(self, value):
        self.context.link_user_action = value
