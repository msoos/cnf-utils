cmake_minimum_required(VERSION 2.6 FATAL_ERROR)

IF(DEFINED CMAKE_BUILD_TYPE)
    SET(CMAKE_BUILD_TYPE ${CMAKE_BUILD_TYPE} CACHE STRING "Choose the type of build, options are: None(CMAKE_CXX_FLAGS or CMAKE_C_FLAGS used) Debug Release RelWithDebInfo MinSizeRel.")
ELSE()
  SET(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "Choose the type of build, options are: None(CMAKE_CXX_FLAGS or CMAKE_C_FLAGS used) Debug Release RelWithDebInfo MinSizeRel.")
ENDIF()

PROJECT(cnf-utils)
#default flags
SET(CMAKE_CXX_FLAGS_RELWITHDEBINFO "-O3 -Wall -Werror -g")
SET(CMAKE_C_FLAGS_RELWITHDEBINFO "-O3 -Wall -Werror -g -std=c99")

# debug flags
SET(CMAKE_CXX_FLAGS_DEBUG "-Wall -Werror -O0 -g")
SET(CMAKE_C_FLAGS_DEBUG "-Wall -Werror -O0 -g -std=c99")

# release flags
SET(CMAKE_CXX_FLAGS_RELEASE "-Wall -Werror -O3 -g0 -fno-exceptions -DNDEBUG -march=native")
SET(CMAKE_C_FLAGS_RELEASE "-Wall -Werror -O3 -g0 -fno-exceptions -DNDEBUG -march=native -std=c99")

# FIND_PACKAGE(OpenMP REQUIRED)
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
# set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")

# find_package( Boost 1.34 REQUIRED COMPONENTS program_options)
# link_directories ( ${Boost_LIBRARY_DIRS} )
# include_directories ( ${Boost_INCLUDE_DIRS} )

add_executable(cnf-cat
    cnf-cat.cc
)
add_executable(cnf-clause
    cnf-clause.cc
)
add_executable(cnf-grep
    cnf-grep.cc
)
add_executable(cnf-shuffle-variables
    cnf-shuffle-variables.cc
)
add_executable(cnf-shuffle-literals
    cnf-shuffle-literals.cc
)
add_executable(cnf-shuffle-clauses
    cnf-shuffle-clauses.cc
)
add_executable(cnf-sort-literals
    cnf-sort-literals.cc
)
add_executable(cnf-sort-clauses
    cnf-sort-clauses.cc
)
add_executable(cnf-propagate
    cnf-propagate.cc
)
add_executable(cnf-stat
    cnf-stat.cc
)
add_executable(cnf-complete
    cnf-complete.cc
)

add_executable(cnf-renumber
    cnf-renumber.c
)

#set(CPACK_PACKAGE_NAME "cnf-utils")
#set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "CNF utilities")
#set(CPACK_PACKAGE_VERSION "1.0.0")
#set(CPACK_PACKAGE_VERSION_MAJOR "1")
#set(CPACK_PACKAGE_VERSION_MINOR "0")
#set(CPACK_PACKAGE_VERSION_PATCH "0")
#set(CPACK_GENERATOR TGZ)
#include(CPack)

