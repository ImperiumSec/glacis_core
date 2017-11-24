# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
#with open(path.join(here, 'README'), encoding='utf-8') as f:
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()


with open(path.join(here,'VERSION')) as version_file:
    version = version_file.read().strip()


install_requires = []
dependency_links = []
with open(path.join(here,'requirements.txt')) as version_file:
    fdeps = version_file.readlines()
    for dep in fdeps:
        tdep = dep.strip()
        if not tdep.startswith("#"):
            if tdep.startswith("git+ssh"):
                dependency_links.append(tdep)
            else:
                install_requires.append(tdep)


setup(
    name='glacis_core',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html

    version=version,
    description='Python library to make managing your queues easy.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/ImperiumSec/glacis_core',

    # Author details
    author='Imperium Sec',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',

        # Pick your license as you wish (should match "license" above)
        'License :: MIT',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='Security Audit SSH',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=install_requires,

    dependency_links=dependency_links,

    include_package_data=True
)