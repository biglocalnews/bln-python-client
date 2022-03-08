import os

import setuptools


def read(file_name):
    """Read the provided file."""
    this_dir = os.path.dirname(__file__)
    file_path = os.path.join(this_dir, file_name)
    with open(file_path) as f:
        return f.read()


def version_scheme(version):
    """Version scheme hack for setuptools_scm.

    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342

    If that issue is resolved, this method can be removed.
    """
    import time

    from setuptools_scm.version import guess_next_version

    if version.exact:
        return version.format_with("{tag}")
    else:
        _super_value = version.format_next_version(guess_next_version)
        now = int(time.time())
        return _super_value + str(now)


def local_version(version):
    """Local version scheme hack for setuptools_scm.

    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342

    If that issue is resolved, this method can be removed.
    """
    return ""


setuptools.setup(
    name="bln",
    version="0.3.2",
    author="Big Local News",
    description="Python client for the biglocalnews.org API",
    license="Apache 2.0 license",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/biglocalnews/sdk/py",
    packages=setuptools.find_packages(exclude=["tests"]),
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
        "Source": "https://github.com/biglocalnews/bln-python-client",
        "Tracker": "https://github.com/biglocalnews/bln-python-client/issues",
    },
    test_suite="tests",
    tests_require=[
        "pytest",
        "pytest-vcr",
        "pytest-cov",
    ],
    setup_requires=["pytest-runner", "setuptools_scm"],
    use_scm_version={"version_scheme": version_scheme, "local_scheme": local_version},
)
