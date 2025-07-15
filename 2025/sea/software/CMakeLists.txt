cmake_minimum_required(VERSION 3.10)
project(BenchmarkProject VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(CheckCXXCompilerFlag)
    check_cxx_compiler_flag("-march=native" COMPILER_SUPPORTS_MARCH_NATIVE)
    if(COMPILER_SUPPORTS_MARCH_NATIVE)
        message(STATUS "Compiler supports -march=native, enabling it.")
        add_compile_options(-march=native)
    endif()


include(cmake/CPM.cmake)
CPMAddPackage("gh:fmtlib/fmt#10.2.1")
CPMAddPackage("gh:lemire/counters#v1.0.1")
CPMAddPackage("gh:fastfloat/fast_float#v8.0.2")

CPMAddPackage(
    NAME curl
    GIT_REPOSITORY https://github.com/curl/curl.git
    GIT_TAG curl-8_14_1  
    OPTIONS
        "BUILD_CURL_EXE OFF" 
        "CMAKE_USE_OPENSSL OFF"
        "CURL_USE_LIBPSL OFF"
)

include_directories(benchmarks src)


add_executable(benchmark benchmarks/benchmark.cpp)
target_link_libraries(benchmark PRIVATE fmt::fmt)
target_link_libraries(benchmark PRIVATE counters)
target_link_libraries(benchmark PRIVATE curl)


add_executable(superscalar benchmarks/superscalar.cpp)
target_link_libraries(superscalar PRIVATE fmt::fmt)
target_link_libraries(superscalar PRIVATE counters)
target_link_libraries(superscalar PRIVATE fast_float)





add_executable(delta benchmarks/delta.cpp)
target_link_libraries(delta PRIVATE fmt::fmt)
target_link_libraries(delta PRIVATE counters)
if (CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang")
    target_compile_options(delta PRIVATE -fno-vectorize)
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(delta PRIVATE -fno-tree-vectorize)
endif()


add_executable(deltavec benchmarks/delta.cpp)
target_link_libraries(deltavec PRIVATE fmt::fmt)
target_link_libraries(deltavec PRIVATE counters)


add_executable(bench_utf16 benchmarks/bench_utf16.cpp)
target_link_libraries(bench_utf16 PRIVATE fmt::fmt)
target_link_libraries(bench_utf16 PRIVATE counters)
if (CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang")
    target_compile_options(bench_utf16 PRIVATE -fno-vectorize)
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(bench_utf16 PRIVATE -fno-tree-vectorize)
endif()

add_executable(bench_speculative benchmarks/bench_speculative.cpp)
target_link_libraries(bench_speculative PRIVATE fmt::fmt)
target_link_libraries(bench_speculative PRIVATE counters)
if (CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang")
    target_compile_options(bench_speculative PRIVATE -fno-vectorize)
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(bench_speculative PRIVATE -fno-tree-vectorize)
endif()



add_executable(bench_random benchmarks/bench_random.cpp)
target_link_libraries(bench_random PRIVATE fmt::fmt)
target_link_libraries(bench_random PRIVATE counters)


add_executable(bench_unroll benchmarks/bench_unroll.cpp)
target_link_libraries(bench_unroll PRIVATE fmt::fmt)
target_link_libraries(bench_unroll PRIVATE counters)

if (CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang")
    target_compile_options(bench_unroll PRIVATE -fno-vectorize -fno-unroll-loops)
elseif (CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(bench_unroll PRIVATE -fno-tree-vectorize -fno-unroll-loops)
endif()
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()


add_executable(bench_misses benchmarks/bench_misses.cpp)
target_link_libraries(bench_misses PRIVATE fmt::fmt)
target_link_libraries(bench_misses PRIVATE counters)


