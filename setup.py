from setuptools import setup

with open('README.txt') as f:
    readme = f.read()

setup(
    name="RhymeHaiker",
    version="1.0.0",
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
            'haiku=poetry.utils.argparser:main',
        ],
    },
    test_suite='tests',
)
