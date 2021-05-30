cmake_minimum_required(VERSION 3.14)

project(PokerHandEvaluator VERSION 0.3.1)

set(CMAKE_BUILD_TYPE  "Release")

# Use C++ 11 Standard to compile
set(CMAKE_CXX_STANDARD 11)

set(CMAKE_C_STANDARD 99)

option(BUILD_TESTS     "Build test ON/OFF"     ON)
option(BUILD_EXAMPLES "Build examples ON/OFF" ON)

# Add the PokerHandEvaluator library
add_library(pheval STATIC
  src/dptables.c
  src/tables_omaha.c
  src/evaluator_omaha.c
  src/evaluator_omaha.cc
  src/evaluator.cc
  src/evaluator5.c
  src/evaluator6.c
  src/evaluator7.c
  src/hash.c
  src/hand.cc
  src/hashtable.c
  src/hashtable5.c
  src/hashtable6.c
  src/hashtable7.c
  src/rank.c
  src/7462.c
)
target_include_directories(pheval PUBLIC 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include/>)
target_compile_options(pheval PUBLIC -O3)
set(PUB_HEADERS include/phevaluator/phevaluator.h
                include/phevaluator/card.h
                include/phevaluator/hand.h
                include/phevaluator/rank.h)
set_target_properties(pheval PROPERTIES
    VERSION ${PROJECT_VERSION}
    PUBLIC_HEADER "${PUB_HEADERS}")

if (BUILD_TESTS)
  include(FetchContent)
  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        release-1.10.0
  )
  # Prevent overriding the parent project's compiler/linker
  # settings on Windows
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
  set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)

  FetchContent_Declare(
    googlebenchmark
    GIT_REPOSITORY https://github.com/google/benchmark.git
    GIT_TAG        v1.5.4
  )
  set(BENCHMARK_ENABLE_INSTALL OFF CACHE BOOL "" FORCE)
  FetchContent_MakeAvailable(googletest googlebenchmark)

  add_executable(unit_tests
    test/evaluation.cc
    test/evaluation_omaha.cc
    test/rank.cc
    test/kev/fast_eval.c
    test/kev/kev_eval.c
  )
  target_compile_options(unit_tests PUBLIC -O3)
  target_link_libraries(unit_tests gtest_main pheval)

  add_test(NAME unit_tests COMMAND unit_tests)

  add_executable(benchmark_phevaluator
    benchmark/benchmark.cc
  )
  target_compile_options(benchmark_phevaluator PUBLIC -O3)
  target_link_libraries(benchmark_phevaluator benchmark pheval)
endif()

if (BUILD_EXAMPLES)
  add_executable(c_example
    examples/c_example.c
  )
  target_link_libraries(c_example pheval)

  add_executable(cpp_example
    examples/cpp_example.cc
  )
  target_link_libraries(cpp_example pheval)

  add_executable(omaha_example
    examples/omaha_example.cc
  )
  target_link_libraries(omaha_example pheval)
endif()

# Install library
if (UNIX)
  include(GNUInstallDirs)
  install(TARGETS pheval
      EXPORT phevalTargets
      LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
      ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
      PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)

  #install find_package script
  install(EXPORT phevalTargets
    NAMESPACE pheval::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/pheval)

  include(CMakePackageConfigHelpers)

  configure_package_config_file(
          ${CMAKE_CURRENT_SOURCE_DIR}/phevalConfig.cmake.in
          ${CMAKE_CURRENT_BINARY_DIR}/phevalConfig.cmake
          INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/pheval
          PATH_VARS
          CMAKE_INSTALL_LIBDIR)

  write_basic_package_version_file(
          ${CMAKE_CURRENT_BINARY_DIR}/phevalConfigVersion.cmake
          COMPATIBILITY SameMajorVersion)

  install(FILES "${CMAKE_CURRENT_BINARY_DIR}/phevalConfig.cmake"
          "${CMAKE_CURRENT_BINARY_DIR}/phevalConfigVersion.cmake"
          DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/pheval")
endif()