from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name="RhymeHaiker",
    version="1.1.1",
    description='A rhyming haiku generator.',
    long_description=readme,
    url='',
    author="pochiyuru",
    license='MIT',
    classifiers=[],
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
