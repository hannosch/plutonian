import unittest


class TestConfigurator(unittest.TestCase):

    def get_module(self):
        import plutonian
        return plutonian

    def make_one(self):
        plutonian = self.get_module()
        return plutonian.Configurator('plutonian')

    def test_package_name(self):
        config = self.make_one()
        self.assertEqual(config.package_name, 'plutonian')

    def test_package(self):
        config = self.make_one()
        plutonian = self.get_module()
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
        plutonian = self.get_module()
        self.assertEqual(package, plutonian)

    def test_maybe_dotted_package(self):
        config = self.make_one()
        plutonian = self.get_module()
        name, package = config.maybe_dotted(plutonian)
        self.assertEqual(name, 'plutonian')
        self.assertEqual(package, plutonian)
