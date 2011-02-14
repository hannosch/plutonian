from setuptools import setup, find_packages

setup(
    name='plutonian',
    version = '1.0a1',
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
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    install_requires=[
        'setuptools',
        'Products.GenericSetup',
        'venusian',
        'zope.dottedname',
        ],
    include_package_data = True,
    zip_safe = False,
    )
