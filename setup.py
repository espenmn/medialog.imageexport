from setuptools import setup, find_packages
import os

version = '0.4'

setup(name='medialog.imageexport',
      version=version,
      description="Export Plone images pil scale imagescale",
      long_description=open(os.path.join("README.rst")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone images preview export',
      author='Espen Moe-Nilssen',
      author_email='espen@medialog.no',
      url='http://www.medialog.no',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['medialog'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
