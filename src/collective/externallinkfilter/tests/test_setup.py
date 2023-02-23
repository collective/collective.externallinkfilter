# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.externallinkfilter.testing import (
    COLLECTIVE_EXTERNALLINKFILTER_INTEGRATION_TESTING,
)  # noqa: E501

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.externallinkfilter is properly installed."""

    layer = COLLECTIVE_EXTERNALLINKFILTER_INTEGRATION_TESTING
