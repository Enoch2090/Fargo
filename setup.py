# -*- encoding: utf-8 -*-
# fargo v0.0.1
# Just watch shows.
# Copyright © 2020, enoch2090.

import io
from setuptools import setup, find_packages


setup(name='fargo',
      version='1.1.0',
      description='A local video playing manager',
      keywords='fargo',
      author='Enoch2090',
      author_email='gyc990926@gmail.com',
      url='https://github.com/Enoch2090/fargo',
      # download_url='https://github.com/gnebbia/kb/archive/v0.1.5.tar.gz',
      license='GPLv3',
      #long_description=io.open('./docs/README.md', 'r', encoding='utf-8').read(),
      # long_description_content_type="text/markdown",
      platforms='any',
      zip_safe=False,
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Operating System :: OS Independent',
                   ],
      packages=find_packages(exclude=()),
      include_package_data=True,
      #install_requires=["colored", "toml", "attr", "attrs"],
      python_requires='>=3.6',
      entry_points={
          'console_scripts': [
              'fargo = fargo.main:main',
          ]
      },
      )
