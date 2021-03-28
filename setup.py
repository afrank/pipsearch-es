import os
import setuptools
from setuptools import setup, find_packages

setup(
    name="pipsearch",
    version="0.0.1",
    description="A suite of tools to scrape data from pypi.org and make it available as a search tool",
    python_requires=">=3.4",
    author="Adam Frank",
    author_email="adam@antilogo.org",
    packages=find_packages(),
    entry_points={"console_scripts": ["pipsearch=pipsearch.client:main",],},
    install_requires=["flask","elasticsearch"],
    extras_require={"test": ["coverage", "pytest", "nose", "simplejson"],},
    project_urls={"Source": "https://github.com/afrank/pipsearch",},
    test_suite="tests.unit",
)

