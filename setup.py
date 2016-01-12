from setuptools import setup, find_packages
from postnl.locations import __version__

setup(
    # package name in pypi
    name='postnl-locations',
    # extract version from module.
    version=__version__,
    description="A Python wrapper for using the PostNL locations SOAP API",
    long_description=open('README.md').read(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python'
    ],
    keywords='',
    author='Martijn Jacobs',
    author_email='martijn@devopsconsulting.nl',
    url='https://github.com/maerteijn/postnl-locations',
    license='BSD',
    # include all packages in the egg, except the tests
    packages=find_packages(
        exclude=['ez_setup', '*tests']),
    # for avoiding conflict have one namespace for all related eggs.
    namespace_packages=['postnl'],
    # include non python files
    include_package_data=True,
    zip_safe=False,
    # specify dependencies
    install_requires=[
        "suds",
    ],
    # mark test target to require extras.
    extras_require={
        'test': ['nose', 'mock', 'coverage']
    },
)
