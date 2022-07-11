import setuptools
import os
import re
import sys
import platform
import subprocess
import warnings

from distutils.version import LooseVersion
from setuptools.command.build_ext import build_ext


class CMakeExtension(setuptools.Extension):
    def __init__(self, name, sourcedir='', cmake_args=(), exclude_arch=False):
        setuptools.Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)
        self.cmake_args = cmake_args
        self.exclude_arch = exclude_arch


class CMakeBuild(build_ext):
    def run(self):
        if os.path.exists('.git'):
            subprocess.check_call(['git', 'submodule', 'update', '--init', '--recursive'])

        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.2.0':
                raise RuntimeError("CMake >= 3.2.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        extdir = os.path.join(extdir, "example")
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir, '-DPYTHON_EXECUTABLE=' + sys.executable]
        cmake_args.extend(ext.cmake_args)

        cfg = 'Debug' if self.debug or os.environ.get("PCU_DEBUG") else 'Release'
        build_args = ['--config', cfg]

        if cfg == 'Debug':
            warnings.warn("Building extension %s in debug mode" % ext.name)

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if os.environ.get('CMAKE_GENERATOR') != "NMake Makefiles":
                if sys.maxsize > 2 ** 32 and not ext.exclude_arch:
                    cmake_args += ['-A', 'x64']
                else:
                    cmake_args += ['-A', 'Win32']
                build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''), self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake'] + cmake_args + [ext.sourcedir], cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)
        print()  # Add an empty line for cleaner output


def main():
    # Check sys.argv for additional arguments to pass to CMake
    if 'EXCLUDE_ARCH' in os.environ or '--exclude-arch' in sys.argv:
        exclude_arch = True
        sys.argv.remove('--exclude-arch')  # Need to remove these not to break setup.py
    else:
        exclude_arch = False
    cmake_args = []
    with open("README.md", "r") as fh:
        long_description = fh.read()

    ############################################################
    # You need to change the code below for your custom module #
    ############################################################

    # The name of your module (directory with an __init__.py). We'll build a C++ extension inside this directory
    # which you can import inside __init__.py
    module_name = 'example'

    setuptools.setup(
        name="numpyeigen-example-project",                     # Full name of your project
        version="0.0.0",                                       # Current version
        author="Francis Williams",                             # Your name
        author_email="francis@fwilliams.info",                 # Your email
        description="Example NumpyEigen Bindings",             # Short Description
        long_description=long_description,                     # Long description which will just be your README.md
        long_description_content_type="text/markdown",         # Long description is Markdown, no need to change
        url="https://github.com/fwilliams/example-python",     # Pointer to website for this project

        # Find all Python packages (directories with __init__.py) except tests to include in the distribution
        packages=setuptools.find_packages(exclude=["tests"]),

        classifiers=[                                          # Used to search on PyPI
            "Programming Language :: C++",
            "Programming Language :: Python :: 3",
        ],

        # Build your package with CMake
        ext_modules=[CMakeExtension(module_name, cmake_args=cmake_args, exclude_arch=exclude_arch)],
        cmdclass=dict(build_ext=CMakeBuild),

        zip_safe=False,     # Can we zip this package or not?
        install_requires=[  # Import dependencies, NumpyEigen requires at least numpy as scipy
            'numpy',
            'scipy'
        ],
        test_suite="tests"  # Name of test module (will run these when you call setup.py test)
    )


if __name__ == "__main__":
    main()

