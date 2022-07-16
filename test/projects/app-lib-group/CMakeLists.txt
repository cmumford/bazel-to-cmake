

cmake_minimum_required (VERSION 3.13)

project(app-lib-group LANGUAGES CXX)

add_library(testlib "")
target_sources(testlib
  PRIVATE
    sum.cc
    sum.h
)

add_executable(test
    main.cc
)
target_link_libraries(test testlib)
