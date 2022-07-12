<h2 align="center">NumpyEigen Example Project</h2>
<h4 align="center"><i>Example Python Module with NumpyEigen</i></h4>

--------------------------

![build workflow](https://github.com/fwilliams/numpyeigen-example-project/actions/workflows/build-wheels-and-publish-to-pipy.yml/badge.svg)

#### Overview
A minimal example project which builds a Python extension with NumpyEigen. The module is called `example` and consists
of two parts:
1. A C++ module called `_example_internal`
2. A Python module called `example` which imports `_example_internal`

This structure allows you to wrap your C++ bindings in a Python function to add extra functionality.

Additionally, this project includes tests (See `/tests` directory) and continuous integration with GitHub actions which
builds on Linux/Mac/Windows and can deploy to PyPI.

#### Modifying this project for your needs
To adapt this project for your own custom module, you need to do the following:
1. Rename `example/` to the name of your module
2. Edit `setup.py` (See comments on where to edit)
3. Edit `CMakeLists.txt` (See comments on where to edit)
4. Edit `tests/test_example.py` (or delete it if you don't want tests)

#### Deploying your package to PyPI
This project can convenient deploy your package to PyPI when you release a new version.
To enable this, first go to:
> Settings > Secrets > Actions

and set the key `PYPI_API_TOKEN` to the API token for your PyPI account. You can get an API
token by going to your [PyPY Account Settings](https://pypi.org/account/login/?next=%2Fmanage%2Faccount%2F)
and scrolling down to the API tokens section.

Once you've set up an API token, you can deploy a new version of your package by creating a
release whose name is of the form `vX.Y.Z` where `X`, `Y`, and `Z` are numbers.

**Important**: When creating a release `vX.Y.Z`, don't forget to update the version in `setup.py` to
match!

When you create such a release, Github Actions will build your package and push the new version to PyPI.