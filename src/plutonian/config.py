from pkg_resources import get_distribution
from Products.GenericSetup.interfaces import EXTENSION
from Products.GenericSetup.registry import _import_step_registry
from Products.GenericSetup.registry import _profile_registry
from Products.GenericSetup.upgrade import _registerUpgradeStep
from Products.GenericSetup.upgrade import UpgradeStep
import venusian
from zope.dottedname.resolve import resolve

from plutonian.gs import run_upgrade


class Configurator(object):

    def __init__(self, package):
        self.package_name, self.package = self.maybe_dotted(package)
        self.package_version = get_distribution(self.package_name).version
        self.policy_profile = u'%s:default' % self.package_name
        self.upgrades = []
        self.ignored_upgrade_profiles = [u'Products.CMFDefault:default',
            u'plone.app.iterate:plone.app.iterate']

    def scan(self, package=None, categories=('plutonian', )):
        if package is None:
            package = self.package
        scanner = venusian.Scanner(config=self)
        scanner.scan(package, categories=categories)

    def maybe_dotted(self, package):
        if isinstance(package, basestring):
            name = package
            package = resolve(name)
        else: # pragma: no cover
            name = package.__name__
        return (name, package)

    def add_import_step(self, name, handler, depends):
        _import_step_registry.registerStep(name, handler=handler,
            dependencies=depends, title=name)

    def add_upgrade_step(self, name, handler, destination):
        step = UpgradeStep(u'Upgrade %s' % name, self.policy_profile,
            str(destination - 1), str(destination), None, handler,
            checker=None, sortkey=0)
        if destination in self.upgrades: # pragma: no cover
            raise ValueError('Duplicate upgrade step to destination %s'
                % destination)
        self.upgrades.append(destination)
        _registerUpgradeStep(step)

    def last_upgrade_to(self):
        return unicode(max(self.upgrades))

    def register_profile(self, package_name=None):
        if package_name is None:
            package_name = self.package_name
        title = '%s:default' % package_name
        _profile_registry.registerProfile('default', title, description=u'',
            path='profiles/default', product=package_name,
            profile_type=EXTENSION)

    def run_all_upgrades(self, setup, skip_policy=False):
        baseline = setup.getBaselineContextID().lstrip('profile-')
        run_upgrade(setup, baseline)
        candidates = set(setup.listProfilesWithUpgrades())
        ignored = set(self.ignored_upgrade_profiles +
            [baseline, self.policy_profile])
        for profile_id in candidates - ignored:
            run_upgrade(setup, profile_id)
        if not skip_policy:
            run_upgrade(setup, self.policy_profile)
