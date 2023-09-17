cmake_minimum_required(VERSION 3.12)
project(MyProject)

set(COBALT_COMPILER "cobaltaot")
set(SOURCE_FILE "init.cobalt")

# Generate the C file from the Cobalt source
add_custom_command(
    OUTPUT init.c
    COMMAND ${COBALT_COMPILER} ${SOURCE_FILE} -o init.c -e
    DEPENDS ${SOURCE_FILE}
    COMMENT "Compiling.."
)

# Compile the C file to an executable
add_executable(app init.c)