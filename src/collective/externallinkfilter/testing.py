# -*- coding: utf-8 -*-
from plone.app.testing import (
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)
from plone.app.testing import login
import collective.externallinkfilter
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD


class CollectiveExternallinkfilterLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=collective.externallinkfilter)

    def setUpPloneSite(self, portal):
        portal.acl_users.userFolderAddUser(
            SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ["Manager"], []
        )
        login(portal, SITE_OWNER_NAME)


COLLECTIVE_EXTERNALLINKFILTER_FIXTURE = CollectiveExternallinkfilterLayer()


COLLECTIVE_EXTERNALLINKFILTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_EXTERNALLINKFILTER_FIXTURE,),
    name="CollectiveExternallinkfilterLayer:IntegrationTesting",
)


COLLECTIVE_EXTERNALLINKFILTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_EXTERNALLINKFILTER_FIXTURE,),
    name="CollectiveExternallinkfilterLayer:FunctionalTesting",
)
