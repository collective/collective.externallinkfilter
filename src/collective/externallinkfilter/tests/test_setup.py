# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from collective.externallinkfilter.testing import COLLECTIVE_EXTERNALLINKFILTER_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.externallinkfilter is properly installed."""

    layer = COLLECTIVE_EXTERNALLINKFILTER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.externallinkfilter is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'collective.externallinkfilter'))

    def test_browserlayer(self):
        """Test that ICollectiveExternallinkfilterLayer is registered."""
        from collective.externallinkfilter.interfaces import (
            ICollectiveExternallinkfilterLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveExternallinkfilterLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_EXTERNALLINKFILTER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('collective.externallinkfilter')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.externallinkfilter is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'collective.externallinkfilter'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveExternallinkfilterLayer is removed."""
        from collective.externallinkfilter.interfaces import \
            ICollectiveExternallinkfilterLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveExternallinkfilterLayer, utils.registered_layers())
