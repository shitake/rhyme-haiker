from setuptools import setup

with open('README.txt') as f:
    readme = f.read()

setup(
    name="poetry",
    version="0.0.1",
    packages=[
        'poetry',
    ],
    author="shitake",
    test_suite='tests',
    long_description=readme
)
