#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'setuptools',
    'SQLAlchemy',
    'bunch',
    'wheel',
    #'spartan==0.0.1'
]

dependency_links = [
    #"git+ssh://git@github.com:xguse/spartan.git@dev#egg=spartan-0.0.1",
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='tsetseDB',
    version='0.0.1',
    description='Code associated with the creation and maintenance of the sample database for our tsetse fly '
                'population genomics project.',
    long_description=readme + '\n\n' + history,
    author='Gus Dunn',
    author_email='wadunn83@gmail.com',
    url='https://github.com/xguse/tsetseDB',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['data/']},
    include_package_data=True,
    install_requires=requirements,
    dependency_links=dependency_links,
    license="MIT",
    zip_safe=False,
    keywords='tsetseDB',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)