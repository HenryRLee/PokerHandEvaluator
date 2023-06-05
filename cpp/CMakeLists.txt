cmake_minimum_required(VERSION 3.14)

project(PokerHandEvaluator VERSION 0.5.2)

set(CMAKE_BUILD_TYPE  "Release")

# Use C++ 11 Standard to compile
set(CMAKE_CXX_STANDARD 11)

set(CMAKE_C_STANDARD 99)

option(BUILD_TESTS    "Build test ON/OFF"     ON)
option(BUILD_EXAMPLES "Build examples ON/OFF" ON)
option(BUILD_OMAHA    "Build Omaha library"   ON)
option(BUILD_PLO5     "Build PLO5 library"    ON)

add_library(pheval STATIC
  src/dptables.c
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

if (BUILD_OMAHA)
  add_library(phevalomaha STATIC
    src/dptables.c
    src/evaluator_omaha.c
    src/evaluator_omaha.cc
    src/tables_omaha.c
    src/hash.c
    src/hand.cc
    src/hashtable.c
    src/rank.c
    src/7462.c
  )
  target_include_directories(phevalomaha PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
      $<INSTALL_INTERFACE:include/>)
  target_compile_options(phevalomaha PUBLIC -O3)
  set(PUB_HEADERS include/phevaluator/phevaluator.h
                  include/phevaluator/card.h
                  include/phevaluator/hand.h
                  include/phevaluator/rank.h)
  set_target_properties(phevalomaha PROPERTIES
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

#execute_process(COMMAND ${CMAKE_COMMAND} -E
#    tar xvzf "${plo5_source_tar}")
#  execute_process(COMMAND ${CMAKE_COMMAND} -E
#    rename "${plo5_source_code}" "${CMAKE_CURRENT_BINARY_DIR}/src/${plo5_source_code}")

  add_library(phevalplo5 STATIC
    src/dptables.c
    src/evaluator_plo5.c
    src/evaluator_plo5.cc
    src/tables_plo5.c
    src/hash.c
    src/hand.cc
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
                  include/phevaluator/hand.h
                  include/phevaluator/rank.h)
  set_target_properties(phevalplo5 PROPERTIES
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

  add_executable(unit_tests
    test/evaluation.cc
    test/evaluation_omaha.cc
    test/evaluation_plo5.cc
    test/rank.cc
    test/kev/fast_eval.c
    test/kev/kev_eval.c
  )
  target_compile_options(unit_tests PUBLIC -O3)
  target_link_libraries(unit_tests gtest_main pheval phevalomaha phevalplo5)

  add_test(NAME unit_tests COMMAND unit_tests)

  add_executable(benchmark_phevaluator
    benchmark/benchmark.cc
  )
  target_compile_options(benchmark_phevaluator PUBLIC -O3)
  target_link_libraries(benchmark_phevaluator benchmark pheval phevalomaha phevalplo5)
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
  target_link_libraries(omaha_example phevalomaha)

  add_executable(plo5_example
    examples/plo5_example.cc
  )
  target_link_libraries(plo5_example phevalplo5)
endif()

# Install library
if (UNIX)
  include(GNUInstallDirs)
  install(TARGETS pheval
      EXPORT phevalTargets
      LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
      ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
      PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)

  install(TARGETS phevalomaha
      EXPORT phevalTargets
      LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
      ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
      PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)

  install(TARGETS phevalplo5
      EXPORT phevalTargets
      LIBRARY DESTINATION ${CMAKE_INSTALL_DIR}
      ARCHIVE DESTINATION ${CMAKE_INSTALL_DIR}
      PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/phevaluator)

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
