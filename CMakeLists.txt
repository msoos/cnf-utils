cmake_minimum_required(VERSION 3.3 FATAL_ERROR)

set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 11)

if(POLICY CMP0048)
    #policy for VERSION in cmake 3.0
    cmake_policy(SET CMP0048 OLD)
endif()

IF(DEFINED CMAKE_BUILD_TYPE)
    SET(CMAKE_BUILD_TYPE ${CMAKE_BUILD_TYPE} CACHE STRING "Choose the type of build, options are: None(CMAKE_CXX_FLAGS or CMAKE_C_FLAGS used) Debug Release RelWithDebInfo MinSizeRel.")
ELSE()
  SET(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "Choose the type of build, options are: None(CMAKE_CXX_FLAGS or CMAKE_C_FLAGS used) Debug Release RelWithDebInfo MinSizeRel.")
ENDIF()

PROJECT(cnf-utils)

add_compile_options("$<$<CONFIG:RELWITHDEBINFO>:-O3>")
add_compile_options("$<$<CONFIG:RELWITHDEBINFO>:-mtune=native>")

add_compile_options("$<$<CONFIG:RELEASE>:-O3>")
add_compile_options("$<$<CONFIG:RELEASE>:-g0>")
add_compile_options("$<$<CONFIG:RELEASE>:-DNDEBUG>")
add_compile_options("$<$<CONFIG:RELEASE>:-mtune=native>")

add_compile_options("$<$<CONFIG:DEBUG>:-O0>")

if (NOT WIN32)
    add_compile_options( -g -pedantic -Wall )
endif()


# add_executable(cnf-cat
#     cnf-cat.cc
# )
# add_executable(cnf-clause
#     cnf-clause.cc
# )
# add_executable(cnf-grep
#     cnf-grep.cc
# )
# add_executable(cnf-shuffle-variables
#     cnf-shuffle-variables.cc
# )
# add_executable(cnf-shuffle-literals
#     cnf-shuffle-literals.cc
# )
# add_executable(cnf-shuffle-clauses
#     cnf-shuffle-clauses.cc
# )
# add_executable(cnf-sort-literals
#     cnf-sort-literals.cc
# )
# add_executable(cnf-sort-clauses
#     cnf-sort-clauses.cc
# )
# add_executable(cnf-propagate
#     cnf-propagate.cc
# )
# add_executable(cnf-stat
#     cnf-stat.cc
# )
# add_executable(cnf-complete
#     cnf-complete.cc
# )
#
# add_executable(cnf-renumber
#     cnf-renumber.c
# )
# add_executable(cnf-fuzz-nossum
#     cnf-fuzz-nossum.cc
# )
#
# add_executable(cnf-fuzz-nossum2
#     cnf-fuzz-nossum2.cc
# )
add_executable(cnf-fuzz-biere
    cnf-fuzz-biere.cc
)

add_executable(sgen4
    sgen4.c
)

add_executable(largefuzzer
    largefuzzer.cpp
)

if (NOT MSVC)
    target_link_libraries(sgen4 m)
endif()
