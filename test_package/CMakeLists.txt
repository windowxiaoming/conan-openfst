cmake_minimum_required(VERSION 3.1.2)
project(conan-openfst-test CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(fst_test fst_test.cc fst_test.h)
target_link_libraries(fst_test CONAN_PKG::OpenFST)
