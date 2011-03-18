from setuptools import setup

setup(
    name='plutonian',
    version = '0.1a2',
    author='Hanno Schlichting',
    author_email='hanno@hannosch.eu',
    description='Pyramid-style development for Plone.',
    long_description=(open('README.txt').read() + '\n' +
        open('CHANGES.txt').read()),
    license='BSD',
    keywords=('pyramid plone'),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        ],
    url='http://pypi.python.org/pypi/plutonian',
    packages=['plutonian'],
    package_dir = {'': 'src'},
    install_requires=[
        'Acquisition',
        'Products.GenericSetup',
        'setuptools',
        'venusian',
        'zope.dottedname',
        ],
    include_package_data = True,
    )
