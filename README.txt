Overview
========

This project aims to bring the fun and ease of the Pyramid development style
into Plone.

Status
------

The work is at a very early alpha stage. There's no promises of API stability
or functionality yet.

Development
-----------

The code and issue tracker can be found at
https://github.com/hannosch/plutonian

Assumptions
-----------

This project assumes you are writing a specific application based on top of
Plone. Your project will consist of configuration, specific deployment
settings, policy code and knowledge about the content structure.

We further assume that non-persistent configuration is generally preferable
over persistent configuration, as it is easier to manage and version.

This approach is very different from the typical Plone development model, in
which you write add-ons for the Plone CMS application.

Usage
-----

Preliminary notes on usage:

In your policy package's (for example named `policy`) `__init__.py` in
the `initialize` function::

    def initialize(context):
        from policy import config
        config.config.register_profile()
        config.config.scan()

For the initialize function to be picked up, you need a `configure.zcml`::

    <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:five="http://namespaces.zope.org/five"
      i18n_domain="policy">

      <five:registerPackage package="." initialize=".initialize"/>

    </configure>

The `config.py` module::

    from plutonian import Configurator

    config = Configurator('policy')

Create a `gs.py`::

    from plone.app.upgrade.utils import loadMigrationProfile
    from plutonian.gs import import_step
    from plutonian.gs import upgrade_to

    from policy.config import config


    def set_profile_version(site):
        setup = getToolByName(site, 'portal_setup')
        setup.setLastVersionForProfile(
            config.policy_profile, config.last_upgrade_to())


    @import_step()
    def various(context):
        if context.readDataFile('policy-various.txt') is None:
            return
        site = context.getSite()
        set_profile_version(site)


    @upgrade_to(2)
    def do_something(context):
        # apply some existing GS files again as they might have changed
        loadMigrationProfile(context, 'profile-policy:default',
            steps=('cssregistry', 'jsregistry', 'plone.app.registry', ))

And finally create a GS profile with a folder structure of `profiles/default`
and put a `metadata.xml` file in there::

    <?xml version="1.0"?>
    <metadata>
      <!-- The version is determined based on the registered upgrade steps
           and must not be set here -->
      <!-- <version>unknown</version> -->
    </metadata>

You also need to create the empty flag file named `policy-various.txt`.
