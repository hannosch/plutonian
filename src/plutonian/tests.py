import unittest

import plutonian


class TestConfigurator(unittest.TestCase):

    def make_one(self):
        from plutonian import Configurator
        return Configurator('plutonian')

    def test_package_name(self):
        config = self.make_one()
        self.assertEqual(config.package_name, 'plutonian')

    def test_package(self):
        config = self.make_one()
        self.assertEqual(config.package, plutonian)

    def test_policy_profile(self):
        config = self.make_one()
        self.assertEqual(config.policy_profile, 'plutonian:default')

    def test_package_version(self):
        from pkg_resources import get_distribution
        config = self.make_one()
        version = get_distribution('plutonian').version
        self.assertEqual(config.package_version, version)

    def test_maybe_dotted_string(self):
        config = self.make_one()
        name, package = config.maybe_dotted('plutonian')
        self.assertEqual(name, 'plutonian')
        self.assertEqual(package, plutonian)

    def test_maybe_dotted_package(self):
        config = self.make_one()
        name, package = config.maybe_dotted(plutonian)
        self.assertEqual(name, 'plutonian')
        self.assertEqual(package, plutonian)
