from Acquisition import aq_get
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


def run_upgrade(setup, profile_id):
    request = aq_get(setup, 'REQUEST')
    request['profile_id'] = profile_id
    upgrades = setup.listUpgrades(profile_id)
    steps = []
    if not upgrades:
        return
    for u in upgrades:
        if isinstance(u, list): # pragma: no cover
            steps.extend([s['id'] for s in u])
        else:
            steps.append(u['id'])
    request.form['upgrades'] = steps
    setup.manage_doUpgrades(request=request)
