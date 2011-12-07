from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='osmine',
      version=version,
      description="OpenSpending Simple Data Mining Framework",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='openspending javascript v8 mining datamining',
      author='Open Knowlegde Foundation',
      author_email='info@openspending.org',
      url='http://openspending.org',
      license='AGPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'openspending.plugins': [
              'mining = osmine.plugin:MiningPlugin'
            ]
        },
      )
