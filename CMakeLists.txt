cmake_minimum_required(VERSION 3.15)
project(numpyeigen-example-project)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_BUILD_TYPE "Release")

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# Download NumpyEigen if we haven't already
set(EXTERNAL_DEP_DIR ${CMAKE_CURRENT_SOURCE_DIR}/external)
include(DownloadExternalDeps)
download_dep(numpyeigen
  GIT_REPOSITORY https://github.com/fwilliams/numpyeigen.git
  GIT_TAG 4916d926aa2b939bd8f625c7537563a1575dafe9
)
list(APPEND CMAKE_MODULE_PATH ${EXTERNAL_DEP_DIR}/numpyeigen/cmake)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
include(numpyeigen) # This will define Eigen3::Eigen if we enabled NPE_WITH_EIGEN


# ###########################################################################################################
# You need to change the following code for your module (e.g. to add more sources, or to rename the module) #
#############################################################################################################

# Create a Python module called _example_internal which will live in the example/ directory
# You can import functions from the internal module in example/__init__.py to publically expose them
npe_add_module(_example_internal
  BINDING_SOURCES
  ${CMAKE_CURRENT_SOURCE_DIR}/src/example.cpp
  )
set_target_properties(_example_internal PROPERTIES COMPILE_FLAGS "-fvisibility=hidden -msse3")

enable_testing()
add_subdirectory(tests)

