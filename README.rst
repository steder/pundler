Pundler_
----------------------

.. image:: https://travis-ci.org/steder/pundler.png

About
======================

Pundler is an attempt to better manage python requirements files.

Pundler is inspired by Ruby's Gem Bundler_.

Specifically the goal is to process ``requirements.yml`` or ``requirements.in``
into a frozen lock file ``requirements.txt`` similar to the way ``Gemfile``
and ``Gemfile.lock`` are related in the ruby world.

The advantage of doing something like this is that your requirements
file specifies only versions of things that you specifically depend on
and dependencies brought in by those dependencies can be easily identified
and separated out.

For example, if I install the requirement ``jinja2==2.7`` I don't actually
care about also installing jinja2's dependency ``markupsafe`` but it will
be installed.  By running Pundler I end up with a nicely pinned ``requirements.txt``
that I can just regenerate from my "real" ``requirements.in`` whenever requirements
I actually care about change.

For example, say I have in ``requirements.in``::

  a==1.0
  b==2.0
  c==3.0

And if we include the dependencies of those packages we have::

  a==1.0
  adep1==1.0
  adep2==1.0
  b==2.0
  bdep1==2.0
  c==3.0

Say we eventually upgrade ``a`` to version 2.0::

  a==2.0
  adep1==1.0
  adep2==1.0
  b==2.0
  bdep1==2.0
  c==3.0

With version ``2.0`` of package ``a`` the dependency ``adep1==1.0`` is no longer needed.  If we have one requirements file with all versions pinned it isn't clear that that dependency can now be removed.

If instead we simply updated the original ``requirements.in`` we could regenerate
the full requirements (as a ``requirements.txt``) and it would be clear that
``adep1==1.0`` was no longer required.

Usage
=======================

Simply run pundler in a directory with your ``requirements.in`` or ``requirements.yml``::

  pundler install

If ``requirements.txt`` doesn't exist ``Pundler`` will process
your ``requirements.yml`` or ``requirements.in`` file and create
a ``requirements.txt`` that has all packages pinned to specific versions and
identifies clearly what depends on what packages depend on what.

(TODO) If ``requirements.txt`` exists than pundler will pass args through
to ``pip install``, essentially::

  pip install -r requirements.txt

------------------------
Updating (TODO)
------------------------

To update all your dependencies::

  pundler update

This should update all unpinned dependencies to the latest
version and appropriately update your generated ``requirements.txt``.

------------------------
Virtualenv
------------------------

By default Pundler operates on the current environment (whatever
`pip` is pointed at the moment.)

If you have a virtualenv enabled when you run ``pundler install``
it will be used.

Example
========================

Given the following ``requirements.in``::

  pyramid==1.4.2
  jinja2
  txtemplate

Pundler will generate the this ``requirements.txt``::

  # requirement 'pyramid==1.4.2' depends on:
  WebOb==1.2.3
  pyramid==1.4.2
  translationstring==1.1
  repoze.lru==0.6
  Mako==0.8.1
  MarkupSafe==0.18
  PasteDeploy==1.5.0
  Chameleon==2.11
  venusian==1.0a8
  zope.deprecation==4.0.2
  zope.interface==4.0.5
  setuptools==0.6c11

  # requirement 'jinja2' depends on:
  jinja2==2.7
  markupsafe==0.18

  # requirement 'txtemplate' depends on:
  genshi==0.7
  #jinja2==2.7
  twisted==13.0.0
  #markupsafe==0.18
  txtemplate==1.0.2
  #zope.interface==4.0.5
  #setuptools==0.6c11

Advanced Configuration (TODO)
=====================================

An alternative to ``requirements.in`` files is a simple
``requirements.yml`` configuration file.

The above example would look like::

  sources:
   - https://pypi.python.org/simple/
  requirements:
   - pyramid==1.4.2
   - jinja2
   - txtemplate

Above, sources is optional.

A more interesting configuration with multiple groups like
development and production would look like this::

  sources:
    - https://pypi.python.org/simple/
  groups:
    development:
      - nose
    production:
      - pyramid==1.4.2
      - jinja2
      - txtemplate
  # by default packages from all groups are installed
  # but you can customize this so that you can install
  # only specific things by defining `targets` and `default`
  targets: # select a target with `pundler install <target>`
    development: # targets are a list of groups to install
     - production
     - development
    production:
     - production
    default: production # what happens if you just do `pundler install`


.. _pundler: http://github.com/steder/pundler
.. _bundler: https://github.com/bundler/bundler
.. _Michael Steder: http://mikesteder.com
