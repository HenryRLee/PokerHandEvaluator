cmake_minimum_required(VERSION 2.8.11)
set(CMAKE_BUILD_TYPE  "Release")

# Download and unpack googletest at configure time
configure_file(CMakeLists.txt.in googletest-download/CMakeLists.txt)
execute_process(COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "CMake step for googletest failed: ${result}")
endif()
execute_process(COMMAND ${CMAKE_COMMAND} --build .
  RESULT_VARIABLE result
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googletest-download )
if(result)
  message(FATAL_ERROR "Build step for googletest failed: ${result}")
endif()

# Prevent overriding the parent project's compiler/linker
# settings on Windows
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

# Add googletest directly to our build. This defines
# the gtest and gtest_main targets.
add_subdirectory(${CMAKE_CURRENT_BINARY_DIR}/googletest-src
                 ${CMAKE_CURRENT_BINARY_DIR}/googletest-build
                 EXCLUDE_FROM_ALL)

configure_file(CMakeLists.txt.in googlebenchmark-download/CMakeLists.txt)
# executing the configuration step
execute_process(
    COMMAND ${CMAKE_COMMAND} -G "${CMAKE_GENERATOR}" .
    RESULT_VARIABLE results
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googlebenchmark-download
)
# checking if the configuration step passed
if(results)
    message(FATAL_ERROR "Configuration step for Benchmark has Failed. ${results}")
endif()
# executing the build step
execute_process(
    COMMAND ${CMAKE_COMMAND} --build . --config Release
    RESULT_VARIABLE results
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/googlebenchmark-download
)
# checking if the build step passed
if(results)
    message(FATAL_ERROR "Build step for Benchmark has Failed. ${results}")
endif()
add_subdirectory(
    ${CMAKE_CURRENT_BINARY_DIR}/googlebenchmark-src
    ${CMAKE_CURRENT_BINARY_DIR}/googlebenchmark-build
    EXCLUDE_FROM_ALL
)

# Use C++ 11 Standard to compile
set(CMAKE_CXX_STANDARD 11)

# Now simply link against gtest or gtest_main as needed. Eg
add_library(pheval SHARED
  src/dptables.c
  src/evaluator.cc
  src/evaluator5.c
  src/evaluator6.c
  src/evaluator7.c
  src/evaluator8.c
  src/evaluator9.c
  src/hash.c
  src/hashtable.c
  src/hashtable5.c
  src/hashtable6.c
  src/hashtable7.c
  src/hashtable8.c
  src/hashtable9.c
)
target_include_directories(pheval PUBLIC include)
target_compile_options(pheval PUBLIC -Ofast)
add_executable(unit_tests
  test/unit_tests.cc
  test/kev/fast_eval.c
  test/kev/kev_eval.c
)
add_executable(benchmark_phevaluator
  benchmark/benchmark.cc
)
target_compile_options(unit_tests PUBLIC -Ofast)
target_link_libraries(unit_tests gtest_main pheval)
target_link_libraries(benchmark_phevaluator benchmark pheval)
add_test(NAME unit_tests COMMAND unit_tests)
