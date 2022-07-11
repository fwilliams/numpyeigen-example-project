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
