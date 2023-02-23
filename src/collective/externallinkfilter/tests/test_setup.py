# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.externallinkfilter.testing import (
    COLLECTIVE_EXTERNALLINKFILTER_INTEGRATION_TESTING,
)  # noqa: E501
import unittest
from plone.app.testing import login
from plone.app.testing import SITE_OWNER_NAME
from doctest import REPORT_NDIFF
from Products.PortalTransforms.tests.utils import normalize_html
from doctest import _ellipsis_match

from collective.externallinkfilter.resolveuid_and_caption import (
    ResolveUIDAndCaptionFilter,
)  # noqa
from doctest import OutputChecker


class TestSetup(unittest.TestCase):
    """Test that collective.externallinkfilter is properly installed."""

    layer = COLLECTIVE_EXTERNALLINKFILTER_INTEGRATION_TESTING

    def _makeParser(self, **kw):
        parser = ResolveUIDAndCaptionFilter(context=self.portal)
        for k, v in kw.items():
            setattr(parser, k, v)
        return parser

    def setUp(self):
        self.portal = self.layer["portal"]
        login(self.portal, SITE_OWNER_NAME)
        self.parser = self._makeParser(
            captioned_images=True, resolve_uids=True
        )
        self.outputchecker = OutputChecker()

        self.doc1 = api.content.create(
            container=self.portal,
            type="Document",
            id="doc1",
            title="Document 1",
        )

        self.doc1_uuid = api.content.get_uuid(self.doc1)

    def _assertTransformsTo(self, input, expected):
        # compare two chunks of HTML ignoring whitespace differences,
        # and with a useful diff on failure
        out = self.parser(input)
        normalized_out = normalize_html(out)
        normalized_expected = normalize_html(expected)
        try:
            self.assertTrue(
                _ellipsis_match(normalized_expected, normalized_out)
            )
        except AssertionError:

            class wrapper(object):
                want = expected

            raise AssertionError(
                self.outputchecker.output_difference(
                    wrapper, out, REPORT_NDIFF
                )
            )

    def test_internal_link_rendering(self):
        """those links entered as internal links should be handled as usual:
        resolve the uid and create an absolute url, including domain,
        to the content object
        """
        text_in = (
            f'<a href="../resolveuid/{self.doc1_uuid}"'
            ' data-linktype="internal"'
            f' data-val="{self.doc1_uuid}">internal</a>'
        )
        text_out = (
            f'<a data-linktype="internal" data-val="{self.doc1_uuid}"'
            f' href="{self.doc1.absolute_url()}">internal</a>'
        )
        self._assertTransformsTo(text_in, text_out)

    def test_external_link_rendering(self):
        """those links entered as external links but that point to a url of
        the portal should be kept as entered, without any try to guess
        its portal content object
        """
        text_in = (
            f'<a href="../resolveuid/{self.doc1_uuid}"'
            ' data-linktype="external"'
            f' data-val="{self.doc1.absolute_url()}">internal</a>'
        )
        text_out = (
            '<a data-linktype="external"'
            f' data-val="{self.doc1.absolute_url()}"'
            f' href="{self.doc1.absolute_url()}">internal</a>'
        )
        self._assertTransformsTo(text_in, text_out)

    def test_external_link_rendering_with_parameters(self):
        """those links entered as external links that point to a url of
        the portal adding some querystring parameters, should be kept
        as entered.
        """
        text_in = (
            f'<a href="../resolveuid/{self.doc1_uuid}"'
            ' data-linktype="external"'
            f' data-val="{self.doc1.absolute_url()}?one=parameter">internal</a>'
        )
        text_out = (
            '<a data-linktype="external"'
            f' data-val="{self.doc1.absolute_url()}?one=parameter"'
            f' href="{self.doc1.absolute_url()}?one=parameter">internal</a>'
        )
        self._assertTransformsTo(text_in, text_out)

    def test_external_link_rendering_to_inexisten_portal_urls(self):
        """those links entered as external links that point to a url that looks like
        is from the portal but it is not to a content-object (imagine you have some other URLs
        handled by an external service, or handled using custom browser views, should be kept
        as entered.
        """
        text_in = (
            f'<a href="../resolveuid/{self.doc1_uuid}"'
            ' data-linktype="external"'
            f' data-val="{self.portal.absolute_url()}/this/url/does/not/exist?one=parameter">internal</a>'
        )
        text_out = (
            '<a data-linktype="external"'
            f' data-val="{self.portal.absolute_url()}/this/url/does/not/exist?one=parameter"'
            f' href="{self.portal.absolute_url()}/this/url/does/not/exist?one=parameter">internal</a>'
        )
        self._assertTransformsTo(text_in, text_out)
