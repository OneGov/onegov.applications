OneGov Applications
===================

Meta-package containing all OneGov Cloud applications.

Read the docs to `find out what constitutes a OneGov Cloud application <http://onegov.readthedocs.io/en/latest/onegov_cloud_modules.html>`_.

The resulting onegov.applications package in PyPI can be used to install all
OneGov applications in one sweep, with the guarantee that all of them were
tested with the same set of dependencies.

That is the meta-package serves as a known good set of dependencies. As such
it allows for applications to be run in the same process using
`onegov.server <http://github.com/onegov/onegov.server>`_.

Unlike other OneGov applications this package does not use Semantic Versioning,
instead opting for a simple year + build number scheme. For example::

  - 2017.1
  - 2017.2
  - 2017.14
  - 2018.1

Before this package is released all contained applications are tested using
their respective unit/integration tests. For this the latest release of
each application is acquired. Therefore each application should be released
separately first, before being included in onegov.applications.

Create a New Release
--------------------

To create a new release for onegov.applications simply run the following
commands in the repository's folder::

  pip install punch.py
  punch --action build

  git push
  git push --tags

Add a New Application
---------------------

To add a new application edit the ``application.json`` file in the
``onegov/applications`` folder. It will then automatically be included in
the build.

In addition, each application has to be added to the .travis.yml build matrix.

Run the Tests
-------------

Install tox and run it::

    pip install tox
    tox

Limit the tests to a specific python version::

    tox -e py27

Conventions
-----------

Onegov Applications follows PEP8 as close as possible. To test for it run::

    tox -e pep8

Build Status
------------

.. image:: https://travis-ci.org/OneGov/onegov.applications.png
  :target: https://travis-ci.org/OneGov/onegov.applications
  :alt: Build Status

Latest PyPI Release
-------------------

.. image:: https://badge.fury.io/py/onegov.applications.svg
    :target: https://badge.fury.io/py/onegov.applications
    :alt: Latest PyPI Release

License
-------
onegov.applications is released under GPLv2
