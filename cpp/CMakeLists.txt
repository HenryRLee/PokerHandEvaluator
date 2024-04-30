cmake_minimum_required(VERSION 3.14)

project(PokerHandEvaluator VERSION 0.6.0)

set(CMAKE_BUILD_TYPE  "Release")

# Use C++ 11 Standard to compile
set(CMAKE_CXX_STANDARD 11)

set(CMAKE_C_STANDARD 99)

option(BUILD_CARD5 "Build 5-card standalone library" ON)
option(BUILD_CARD6 "Build 6-card standalone library" ON)
option(BUILD_CARD7 "Build 7-card standalone library" ON)
option(BUILD_PLO4 "Build PLO4 library" ON)
option(BUILD_PLO5 "Build PLO5 library" ON)
option(BUILD_PLO6 "Build PLO6 library" ON)
option(BUILD_TESTS "Build test ON/OFF" ON)
option(BUILD_EXAMPLES "Build examples ON/OFF" ON)

add_library(pheval STATIC
  src/card_sampler.cc
  src/dptables.c
  src/evaluator5.cc
  src/evaluator5.c
  src/evaluator6.cc
  src/evaluator6.c
  src/evaluator7.cc
  src/evaluator7.c
  src/tables_bitwise.c
  src/hash.c
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
                include/phevaluator/card_sampler.h
                include/phevaluator/rank.h)
set_target_properties(pheval PROPERTIES
    VERSION ${PROJECT_VERSION}
    PUBLIC_HEADER "${PUB_HEADERS}")

if (BUILD_CARD5)
  add_library(pheval5 STATIC
    src/dptables.c
    src/tables_bitwise.c
    src/evaluator5.c
    src/evaluator5.cc
    src/hashtable5.c
    src/hashtable.c
    src/hash.c
  )
  target_include_directories(pheval5 PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include/>)
  target_compile_options(pheval5 PUBLIC -O3)
  set(PUB_HEADERS include/phevaluator/phevaluator.h
                  include/phevaluator/card.h
                  include/phevaluator/rank.h)
  set_target_properties(pheval5 PROPERTIES
      VERSION ${PROJECT_VERSION}
      PUBLIC_HEADER "${PUB_HEADERS}")
endif()

if (BUILD_CARD6)
  add_library(pheval6 STATIC
    src/dptables.c
    src/tables_bitwise.c
    src/evaluator6.c
    src/evaluator6.cc
    src/hashtable6.c
    src/hashtable.c
    src/hash.c
  )
  target_include_directories(pheval6 PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include/>)
  target_compile_options(pheval6 PUBLIC -O3)
  set(PUB_HEADERS include/phevaluator/phevaluator.h
                  include/phevaluator/card.h
                  include/phevaluator/rank.h)
  set_target_properties(pheval6 PROPERTIES
      VERSION ${PROJECT_VERSION}
      PUBLIC_HEADER "${PUB_HEADERS}")
endif()

if (BUILD_CARD7)
  add_library(pheval7 STATIC
    src/dptables.c
    src/tables_bitwise.c
    src/evaluator7.c
    src/evaluator7.cc
    src/hashtable7.c
    src/hashtable.c
    src/hash.c
  )
  target_include_directories(pheval7 PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include/>)
  target_compile_options(pheval7 PUBLIC -O3)
  set(PUB_HEADERS include/phevaluator/phevaluator.h
                  include/phevaluator/card.h
                  include/phevaluator/rank.h)
  set_target_properties(pheval7 PROPERTIES
      VERSION ${PROJECT_VERSION}
      PUBLIC_HEADER "${PUB_HEADERS}")
endif()

if (BUILD_PLO4)
  add_library(phevalplo4 STATIC
    src/card_sampler.cc
    src/dptables.c
    src/evaluator_plo4.c
    src/evaluator_plo4.cc
    src/tables_bitwise.c
    src/tables_plo4.c
    src/hash.c
    src/hashtable.c
    src/rank.c
    src/7462.c
  )
  target_include_directories(phevalplo4 PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include/>)
  target_compile_options(phevalplo4 PUBLIC -O3)
  set(PUB_HEADERS include/phevaluator/phevaluator.h
                  include/phevaluator/card.h
                  include/phevaluator/card_sampler.h
                  include/phevaluator/rank.h)
  set_target_properties(phevalplo4 PROPERTIES
      VERSION ${PROJECT_VERSION}
      PUBLIC_HEADER "${PUB_HEADERS}")
endif()

if (BUILD_PLO5)
  set(plo5_source_tar "${CMAKE_CURRENT_SOURCE_DIR}/src/tables_plo5.tar.gz")
  set(plo5_source_code "${CMAKE_CURRENT_SOURCE_DIR}/src/tables_plo5.c")
  add_custom_command(
    OUTPUT "${plo5_source_code}"
    COMMAND ${CMAKE_COMMAND} -E tar xvzf "${plo5_source_tar}"
    MAIN_DEPENDENCY ${plo5_source_tar}
    COMMENT "Unpacking ${plo5_source_code}"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/src"
  )

  add_library(phevalplo5 STATIC
    src/card_sampler.cc
    src/dptables.c
    src/evaluator_plo5.c
    src/evaluator_plo5.cc
    src/tables_bitwise.c
    src/tables_plo5.c
    src/hash.c
    src/hashtable.c
    src/rank.c
    src/7462.c
  )
  target_include_directories(phevalplo5 PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include/>)
  target_compile_options(phevalplo5 PUBLIC -O3)
  set(PUB_HEADERS include/phevaluator/phevaluator.h
                  include/phevaluator/card.h
                  include/phevaluator/card_sampler.h
                  include/phevaluator/rank.h)
  set_target_properties(phevalplo5 PROPERTIES
      VERSION ${PROJECT_VERSION}
      PUBLIC_HEADER "${PUB_HEADERS}")
endif()

if (BUILD_PLO6)
  set(plo6_source_tar "${CMAKE_CURRENT_SOURCE_DIR}/src/tables_plo6.tar.gz")
  add_custom_command(
    OUTPUT "${CMAKE_CURRENT_SOURCE_DIR}/src/tables_plo6.c"
    COMMAND ${CMAKE_COMMAND} -E tar xvzf "${plo6_source_tar}"
    MAIN_DEPENDENCY ${plo6_source_tar}
    COMMENT "Unpacking ${plo6_source_tar}"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/src"
  )

  add_library(phevalplo6 STATIC
    src/card_sampler.cc
    src/dptables.c
    src/evaluator_plo6.c
    src/evaluator_plo6.cc
    src/tables_bitwise.c
    src/tables_plo6.c
    src/hash.c
    src/hashtable.c
    src/rank.c
    src/7462.c
  )
  target_include_directories(phevalplo6 PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include/>)
  target_compile_options(phevalplo6 PUBLIC -O3)
  set(PUB_HEADERS include/phevaluator/phevaluator.h
                  include/phevaluator/card.h
                  include/phevaluator/card_sampler.h
                  include/phevaluator/rank.h)
  set_target_properties(phevalplo6 PROPERTIES
      VERSION ${PROJECT_VERSION}
      PUBLIC_HEADER "${PUB_HEADERS}")
endif()

if (BUILD_TESTS)
  include(FetchContent)
  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        release-1.12.1
  )
  # Prevent overriding the parent project's compiler/linker
  # settings on Windows
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
  set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)

  FetchContent_Declare(
    googlebenchmark
    GIT_REPOSITORY https://github.com/google/benchmark.git
    GIT_TAG        v1.8.0
  )
  set(BENCHMARK_ENABLE_INSTALL OFF CACHE BOOL "" FORCE)
  FetchContent_MakeAvailable(googletest googlebenchmark)

  if (BUILD_PLO4)
    set(unit_tests_source_plo4 test/evaluation_plo4.cc)
    set(benchmark_source_plo4 benchmark/benchmark_plo4.cc)
    set(library_plo4 phevalplo4)
  endif()

  if (BUILD_PLO5)
    set(unit_tests_source_plo5 test/evaluation_plo5.cc)
    set(benchmark_source_plo5 benchmark/benchmark_plo5.cc)
    set(library_plo5 phevalplo5)
  endif()

  if (BUILD_PLO6)
    set(unit_tests_source_plo6 test/evaluation_plo6.cc)
    set(benchmark_source_plo6 benchmark/benchmark_plo6.cc)
    set(library_plo6 phevalplo6)
  endif()

  add_executable(unit_tests
    test/evaluation.cc
    ${unit_tests_source_plo4}
    ${unit_tests_source_plo5}
    ${unit_tests_source_plo6}
    test/rank.cc
    test/kev/fast_eval.c
    test/kev/kev_eval.c
  )
  target_compile_options(unit_tests PUBLIC -O3)
  target_link_libraries(unit_tests gtest_main pheval
    ${library_plo4}
    ${library_plo5}
    ${library_plo6}
  )

  add_test(NAME unit_tests COMMAND unit_tests)

  add_executable(benchmark_phevaluator
    benchmark/benchmark.cc
    ${benchmark_source_plo4}
    ${benchmark_source_plo5}
    ${benchmark_source_plo6}
  )
  target_compile_options(benchmark_phevaluator PUBLIC -O3)
  target_link_libraries(benchmark_phevaluator benchmark pheval
    ${library_plo4}
    ${library_plo5}
    ${library_plo6}
  )

  set(CMAKE_BUILD_TYPE "DEBUG") # Trying to enable assert in the following tests

  if (BUILD_CARD5)
    add_executable(unit_tests_evaluator5_standalone
      test/evaluation5_standalone.cc
      test/kev/fast_eval.c
      test/kev/kev_eval.c
    )
    target_compile_options(unit_tests_evaluator5_standalone PUBLIC -O3)
    target_link_libraries(unit_tests_evaluator5_standalone pheval5)
  endif()

  if (BUILD_CARD6)
    add_executable(unit_tests_evaluator6_standalone
      test/evaluation6_standalone.cc
      test/kev/fast_eval.c
      test/kev/kev_eval.c
    )
    target_compile_options(unit_tests_evaluator6_standalone PUBLIC -O3)
    target_link_libraries(unit_tests_evaluator6_standalone pheval6)
  endif()

  if (BUILD_CARD6)
    add_executable(unit_tests_evaluator7_standalone
      test/evaluation7_standalone.cc
      test/kev/fast_eval.c
      test/kev/kev_eval.c
    )
    target_compile_options(unit_tests_evaluator7_standalone PUBLIC -O3)
    target_link_libraries(unit_tests_evaluator7_standalone pheval7)
  endif()
endif()

if (BUILD_EXAMPLES)
  set(CMAKE_BUILD_TYPE "DEBUG") # Trying to enable assert in the following tests

  add_executable(c_example
    examples/c_example.c
  )
  target_link_libraries(c_example pheval)

  add_executable(cpp_example
    examples/cpp_example.cc
  )
  target_link_libraries(cpp_example pheval)

  if (BUILD_CARD5)
    add_executable(evaluator5_standalone_example
      examples/evaluator5_standalone_example.cc
    )
    target_link_libraries(evaluator5_standalone_example pheval5)
  endif()

  if (BUILD_CARD6)
    add_executable(evaluator6_standalone_example
      examples/evaluator6_standalone_example.cc
    )
    target_link_libraries(evaluator6_standalone_example pheval6)
  endif()

  if (BUILD_CARD7)
    add_executable(evaluator7_standalone_example
      examples/evaluator7_standalone_example.cc
    )
    target_link_libraries(evaluator7_standalone_example pheval7)
  endif()

  if (BUILD_PLO4)
    add_executable(plo4_example
      examples/plo4_example.cc
    )
    target_link_libraries(plo4_example phevalplo4)

    add_executable(omaha_example
      examples/omaha_example.cc
    )
    target_link_libraries(omaha_example phevalplo4)
  endif()

  if (BUILD_PLO5)
    add_executable(plo5_example
      examples/plo5_example.cc
    )
    target_link_libraries(plo5_example phevalplo5)
  endif()

  if (BUILD_PLO6)
    add_executable(plo6_example
      examples/plo6_example.cc
    )
    target_link_libraries(plo6_example phevalplo6)
  endif()
endif()

# Install library
if (UNIX)
  include(GNUInstallDirs)
  install(TARGETS pheval
      EXPORT phevalTargets
      LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
      ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
      PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)

  if (BUILD_PLO4)
    install(TARGETS phevalplo4
        EXPORT phevalTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)
  endif()

  if (BUILD_PLO5)
    install(TARGETS phevalplo5
        EXPORT phevalTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)
  endif()

  if (BUILD_PLO6)
    install(TARGETS phevalplo6
        EXPORT phevalTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)
  endif()

  #install find_package script
  install(EXPORT phevalTargets
    NAMESPACE phevaluator::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/phevaluator)

  include(CMakePackageConfigHelpers)

  configure_package_config_file(
          ${CMAKE_CURRENT_SOURCE_DIR}/phevaluatorConfig.cmake.in
          ${CMAKE_CURRENT_BINARY_DIR}/phevaluatorConfig.cmake
          INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/phevaluator
          PATH_VARS
          CMAKE_INSTALL_LIBDIR)

  write_basic_package_version_file(
          ${CMAKE_CURRENT_BINARY_DIR}/phevaluatorConfigVersion.cmake
          COMPATIBILITY SameMajorVersion)

  install(FILES "${CMAKE_CURRENT_BINARY_DIR}/phevaluatorConfig.cmake"
          "${CMAKE_CURRENT_BINARY_DIR}/phevaluatorConfigVersion.cmake"
          DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/phevaluator")
endif()
