from setuptools import setup, find_packages

import distutils.command.bdist_conda


with open('../README.md') as f:
    long_description = f.read()

setup(name='beautiful_ast',
      version='1.0.3',
      description='Beautiful AST generator',
      author='Gleb Marin',
      author_email='glebmar2001@gmail.com',
      license='MIT',
      url='https://github.com/Glebanister/hse-advanced-python/tree/hw-01-beatiful-ast/hw01',
      packages=find_packages(),
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
      conda_buildnum=1
      )
