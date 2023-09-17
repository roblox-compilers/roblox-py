cmake_minimum_required(VERSION 3.12)
project(MyProject)

if (NOT COBALT_INCLUDES)
    message(FATAL_ERROR "Please provide Cobalt include path like `-DCOBALT_INCLUDES=/path/to/cobalt/includes`")
endif()
set(CMAKE_C_FLAGS "-w -O3 -I${COBALT_INCLUDES}")
message("CMAKE_C_FLAGS: ${CMAKE_C_FLAGS}")
add_subdirectory(src)