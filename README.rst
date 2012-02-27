Overview
========

This project aims to bring some of the fun and ease of the Pyramid
development style into Plone.

At its current stage it only has some helpers to simplify GenericSetup
handling, especially around upgrade steps.

Development
-----------

The code and issue tracker can be found at
https://github.com/hannosch/plutonian

Assumptions
-----------

This project assumes you are writing a specific application based on top of
Plone. You have one policy package that manages the specifics of one site.

This library is not useful or intended for writing reusable add-ons for Plone.

Usage
-----

Preliminary notes on using the GenericSetup helpers:

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
    from Products.CMFCore.utils import getToolByName

    from policy.config import config


    def set_profile_version(site):
        # while creating a new site, assign the last version number and thus
        # treat it as not needing any of the existing upgrade steps
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
        # apply some existing GS files again from the policy profile if they
        # have changed or do anything else you might need to do
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

The `upgrade_to` decorator takes integers. No number can be taken multiple
times, but there can be numbers missing in the sequence.

The upgrade steps are registered in the normal place and can be run via the
`portal_setup` ZMI screens. As an alternative you can create a `zopectl`
command to run them from the command line. In your `setup.py` add an entry::

    entry_points="""
    [zopectl.command]
    upgrade = policy.commands:upgrade
    """

And create a `commands.py` with the function::

    import logging
    import sys

    import transaction
    from AccessControl.SecurityManagement import newSecurityManager
    from zope.site.hooks import setHooks
    from zope.site.hooks import setSite

    logger = logging.getLogger()


    def _setup(app, site=None):
        """Set up our environment. Create a request, log in as admin and set
        the traversal hooks on the site.
        """
        # Do not import this at the module level, or you get a demo storage
        # ZODB instead of the real one!
        from Testing import makerequest
        app = makerequest.makerequest(app)

        # Login as admin
        admin = app.acl_users.getUserById('admin')
        if admin is None:
            logger.error("No user called `admin` found in the database.")
            sys.exit(1)

        # Wrap the admin in the right context
        if site is not None:
            admin = admin.__of__(site.acl_users)
            site = app[site.getId()]
        else:
            admin = admin.__of__(app.acl_users)
        newSecurityManager(None, admin)

        # Set up local site manager, skins and language
        if site is not None:
            setHooks()
            setSite(site)
            site.setupCurrentSkin(site.REQUEST)
            site.REQUEST['HTTP_ACCEPT_LANGUAGE'] = site.Language()

        return (app, site)


    def upgrade(app, args):
        # Display all messages on stderr
        logger.setLevel(logging.DEBUG)
        logger.handlers[0].setLevel(logging.DEBUG)

        existing = app.objectValues('Plone Site')
        site = existing and existing[0] or None
        if site is None:
            logger.error("No Plone site found in the database.")
            sys.exit(1)

        _, site = _setup(app, site)

        from policy.config import config

        logger.info("Starting the upgrade.\n\n")
        setup = site.portal_setup
        config.run_all_upgrades(setup)
        logger.info("Ran upgrade steps.")

        # Recook resources, as some CSS/JS files might have changed.
        site.portal_css.cookResources()
        site.portal_javascripts.cookResources()
        logger.info("Resources recooked.")

        transaction.get().note('Upgraded profiles and recooked resources.')
        transaction.get().commit()
        sys.exit(0)


You can then call this script via::

    bin/instance upgrade

It will currently recook the CSS/JS resources on each run, but otherwise has
no ill side-effects, so you can run it as many times as you want.
