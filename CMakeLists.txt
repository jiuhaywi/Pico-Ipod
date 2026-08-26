cmake_minimum_required(VERSION 3.13)
# Include the Pico SDK initializer
include(pico_sdk_import.cmake)
project(pico_ipod C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
# Initialize the Pico SDK
pico_sdk_init()
# Define your project executable and its source files
add_executable(pico_ipod
    src/main.cpp
    src/display.cpp
    src/input.cpp
  )
# Tell CMake to look in src/ for header files (.hpp)
target_include_directories(pico_ipod PRIVATE src)
# Link Pico hardware drivers
target_link_libraries(pico_ipod
    pico_stdlib
    hardware_spi
    hardware_gpio
    hardware_pwm
)
# Generate .uf2, .bin, and .hex files automatically
pico_add_extra_outputs(pico_ipod)
