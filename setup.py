import os

import setuptools


def read(file_name):
    """Read the provided file."""
    this_dir = os.path.dirname(__file__)
    file_path = os.path.join(this_dir, file_name)
    with open(file_path) as f:
        return f.read()


setuptools.setup(
    name="bln",
    version="0.3.2",
    author="Big Local News",
    description="Python client for the biglocalnews.org API",
    license="Apache 2.0 license",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/biglocalnews/sdk/py",
    packages=setuptools.find_packages(),
    scripts=[
        "scripts/bln",
        "scripts/git-bln",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
    ],
    project_urls={
        "Maintainer": "https://github.com/biglocalnews",
        "Source": "https://github.com/biglocalnews/sdk",
        "Tracker": "https://github.com/biglocalnews/sdk/issues",
    },
    test_suite="tests",
    tests_require=[
        "pytest",
        "pytest-vcr",
        "pytest-cov",
    ],
    setup_requires=[
        "pytest-runner",
    ],
)
