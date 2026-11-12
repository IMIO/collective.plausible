from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import collective.plausible


class CollectivePlausibleLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.plausible)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.plausible:default")
        applyProfile(portal, "collective.plausible:testing")


COLLECTIVE_PLAUSIBLE_FIXTURE = CollectivePlausibleLayer()


COLLECTIVE_PLAUSIBLE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PLAUSIBLE_FIXTURE,),
    name="CollectivePlausibleLayer:IntegrationTesting",
)


COLLECTIVE_PLAUSIBLE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_PLAUSIBLE_FIXTURE,),
    name="CollectivePlausibleLayer:FunctionalTesting",
)
