import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='bln',
    version='0.1.9',
    author='Daniel Jenson',
    author_email='daniel.a.jenson@gmail.com',
    description='Big Local News Python SDK',
    license='GNU GPLv3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    platform='OS Independent',
    url='https://github.com/biglocalnews/sdk/py',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'pandas',
        'xlrd',
    ],
)
