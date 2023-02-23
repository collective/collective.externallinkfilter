.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://github.com/collective/collective.externallinkfilter/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.externallinkfilter/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/collective.externallinkfilter/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.externallinkfilter?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/collective.externallinkfilter/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/collective.externallinkfilter

.. image:: https://img.shields.io/pypi/v/collective.externallinkfilter.svg
    :target: https://pypi.python.org/pypi/collective.externallinkfilter/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.externallinkfilter.svg
    :target: https://pypi.python.org/pypi/collective.externallinkfilter
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.externallinkfilter.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.externallinkfilter.svg
    :target: https://pypi.python.org/pypi/collective.externallinkfilter/
    :alt: License


=============================
collective.externallinkfilter
=============================

This addon overrides Plone's default `resolve_uid_and_caption` filter, to not to try to transform external links
entered through TinyMCE.

This product is a workaround of the following bug: https://github.com/plone/mockup/issues/1116


Documentation
-------------

Full documentation for end users can be found in the "docs" folder.



Installation
------------

Install collective.externallinkfilter by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.externallinkfilter


and then running ``bin/buildout``

This product will be enabled when you restart the instance. There is no need to install any profile.

To uninstall this product just remove it from your buildout file and run buildout.


Authors
-------

Mikel Larreategi



Contribute
----------

- Issue Tracker: https://github.com/collective/collective.externallinkfilter/issues
- Source Code: https://github.com/collective/collective.externallinkfilter
- Documentation: https://docs.plone.org/foo/bar


License
-------

The project is licensed under the GPLv2.
