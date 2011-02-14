import venusian


class import_step(object):

    def __init__(self, depends=('toolset', 'types', 'workflow')):
        self.depends = depends

    def register(self, scanner, name, wrapped):
        config = scanner.config
        name = wrapped.__module__ + name
        config.add_import_step(name, wrapped, self.depends)

    def __call__(self, wrapped):
        venusian.attach(wrapped, self.register, category='plutonian')
        return wrapped


class upgrade_to(object):

    def __init__(self, destination):
        self.destination = destination

    def register(self, scanner, name, wrapped):
        config = scanner.config
        config.add_upgrade_step(name, wrapped, self.destination)

    def __call__(self, wrapped):
        venusian.attach(wrapped, self.register, category='plutonian')
        return wrapped
