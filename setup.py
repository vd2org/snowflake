# Copyright (C) 2021 by Ivan.
# This file is part of Snowflake package.
# Snowflake is released under the MIT License (see LICENSE).


from os.path import join, dirname

import setuptools

setuptools.setup(
    name='snowflake-id',
    version='0.0.2',
    author='Vd',
    author_email='vd@vd2.org',
    url='https://github.com/vd2org/snowflake',
    license='MIT',
    description='The Snowflake generator done right.',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Database',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
