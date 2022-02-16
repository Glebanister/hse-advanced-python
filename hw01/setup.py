#!/usr/bin/env python3

from setuptools import setup, find_packages

import distutils.command.bdist_conda


with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = [
        line.strip()
        for line in f.readlines()
        if line.strip() and not line.strip().startswith('#')
    ]

print(requirements)

setup(name='beautiful_ast',
      version='1.0.5',
      description='Beautiful AST generator',
      author='Gleb Marin',
      author_email='glebmar2001@gmail.com',
      license='MIT',
      url='https://github.com/Glebanister/hse-advanced-python/tree/hw-01-beatiful-ast/hw01',
      package_dir={'': 'src'},
      packages=find_packages(where='src'),
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      include_package_data=True,
      distclass=distutils.command.bdist_conda.CondaDistribution,
      conda_buildnum=1,
      python_requires=">=3.9",
      )
