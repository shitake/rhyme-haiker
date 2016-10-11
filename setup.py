from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name="RhymeHaiker",
    version="2.0.0",
    description='A rhyming haiku generator.',
    long_description=readme,
    url='',
    author="pochiyuru",
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: Japanese',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications'
    ],
    keywords='rhyme haiku',
    packages=[
        'poetry',
    ],
    install_requires=[],
    data_files=[],
    entry_points={
        'console_scripts': [
            'haiku=poetry.utils.argparsers:main',
        ],
    },
    test_suite='tests',
)
