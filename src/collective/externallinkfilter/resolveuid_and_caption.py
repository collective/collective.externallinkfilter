# -*- coding: utf-8 -*-
from DocumentTemplate.DT_Var import newline_to_br
from DocumentTemplate.html_quote import html_quote
from plone.outputfilters.filters.resolveuid_and_caption import (
    ResolveUIDAndCaptionFilter as Base,
)
from zope.interface import implementer
from plone.outputfilters.interfaces import IFilter
from plone.outputfilters.filters.resolveuid_and_caption import (
    ResolveUIDAndCaptionFilter as Base,
)

from Acquisition import aq_acquire
from bs4 import BeautifulSoup

from plone.outputfilters.interfaces import IFilter
from Products.CMFPlone.utils import safe_text
from zope.interface import implementer

import re
from bs4 import BeautifulSoup


@implementer(IFilter)
class ResolveUIDAndCaptionFilter(Base):
    def __call__(self, data):
        data = re.sub(r"<([^<>\s]+?)\s*/>", self._shorttag_replace, data)
        soup = BeautifulSoup(safe_text(data), "html.parser")
        for elem in soup.find_all(["a", "area"]):
            attributes = elem.attrs
            if attributes.get("data-linktype", "") == "external":
                attributes["href"] = attributes.get("data-val")
            else:
                href = attributes.get("href")
                if not href:
                    continue
                if (
                    not href.startswith("mailto<")
                    and not href.startswith("mailto:")
                    and not href.startswith("tel:")
                    and not href.startswith("#")
                ):
                    attributes["href"] = self._render_resolveuid(href)

        for elem in soup.find_all(["source", "img"]):
            # handles srcset attributes, not src
            # parent of SOURCE is picture here.
            # SRCSET on source/img specifies one or more images (see below).
            attributes = elem.attrs
            srcset = attributes.get("srcset")
            if not srcset:
                continue
            # https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images
            # [(src1, 480w), (src2, 360w)]
            srcs = [
                src.strip().split()
                for src in srcset.strip().split(",")
                if src.strip()
            ]
            for idx, elm in enumerate(srcs):
                image_url = elm[0]
                image, fullimage, src, description = self.resolve_image(
                    image_url
                )
                srcs[idx][0] = src
            attributes["srcset"] = ",".join(" ".join(src) for src in srcs)
        for elem in soup.find_all(["source", "iframe", "audio", "video"]):
            # parent of SOURCE is video or audio here.
            # AUDIO/VIDEO can also have src attribute.
            # IFRAME is used to embed PDFs.
            attributes = elem.attrs
            src = attributes.get("src")
            if not src:
                continue
            attributes["src"] = self._render_resolveuid(src)
        for elem in soup.find_all(["img", "picture"]):
            if elem.name == "picture":
                img_elem = elem.find("img")
            else:
                img_elem = elem
            # handle src attribute
            attributes = img_elem.attrs
            src = attributes.get("src", "")
            image, fullimage, src, description = self.resolve_image(src)
            attributes["src"] = src
            if image and hasattr(image, "width"):
                if "width" not in attributes:
                    attributes["width"] = image.width
                if "height" not in attributes:
                    attributes["height"] = image.height
            if fullimage is not None:
                # Check to see if the alt / title tags need setting
                title = safe_text(aq_acquire(fullimage, "Title")())
                if not attributes.get("alt"):
                    # bettr an emty alt tag than none. This avoid's screen readers
                    # to read the file name instead. A better fallback would be
                    # a fallback alt text comming from the img object.
                    attributes["alt"] = ""
                if "title" not in attributes:
                    attributes["title"] = title

            # handle captions
            if "captioned" in elem.attrs.get("class", []):
                caption = description
                caption_manual_override = attributes.get(
                    "data-captiontext", ""
                )
                if caption_manual_override:
                    caption = caption_manual_override
                # Check if the image needs to be captioned
                if self.captioned_images and caption:
                    options = {}
                    options["tag"] = elem.prettify()
                    options["caption"] = newline_to_br(html_quote(caption))
                    options["class"] = " ".join(attributes["class"])
                    del attributes["class"]
                    if elem.name == "picture":
                        elem.append(img_elem)
                    captioned = BeautifulSoup(
                        self.captioned_image_template(**options), "html.parser"
                    )

                    # if we are a captioned image within a link, remove and occurrences
                    # of a tags inside caption template to preserve the outer link
                    if bool(elem.find_parent("a")) and bool(
                        captioned.find("a")
                    ):
                        captioned.a.unwrap()
                    if elem.name == "picture":
                        del captioned.picture.img["class"]
                    else:
                        del captioned.img["class"]
                    elem.replace_with(captioned)
        return str(soup)
