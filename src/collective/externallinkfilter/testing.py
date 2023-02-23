# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.externallinkfilter


class CollectiveExternallinkfilterLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.externallinkfilter)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.externallinkfilter:default')


COLLECTIVE_EXTERNALLINKFILTER_FIXTURE = CollectiveExternallinkfilterLayer()


COLLECTIVE_EXTERNALLINKFILTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_EXTERNALLINKFILTER_FIXTURE,),
    name='CollectiveExternallinkfilterLayer:IntegrationTesting',
)


COLLECTIVE_EXTERNALLINKFILTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_EXTERNALLINKFILTER_FIXTURE,),
    name='CollectiveExternallinkfilterLayer:FunctionalTesting',
)


COLLECTIVE_EXTERNALLINKFILTER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_EXTERNALLINKFILTER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveExternallinkfilterLayer:AcceptanceTesting',
)
