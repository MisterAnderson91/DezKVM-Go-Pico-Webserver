cmake_minimum_required(VERSION 3.13)

# Set PICO_SDK_PATH to the submodule
set(PICO_SDK_PATH ${CMAKE_CURRENT_LIST_DIR}/pico-sdk)

# Include Pico SDK import before project declaration
include(pico_sdk_import.cmake)

project(dezkvm_pico C CXX ASM)

# Initialize the Pico SDK
pico_sdk_init()

# Define the target executable
add_executable(dezkvm_pico
    src/main.c
    src/fs_custom.c
    src/usb_descriptors.c
    src/dhserver.c
    src/dnserver.c
    src/rndis_reports.c
)

# Pull in our pico_stdlib and tinyusb network/lwip dependencies
target_link_libraries(dezkvm_pico
    pico_stdlib
    hardware_pwm
    tinyusb_device
    tinyusb_board
    pico_lwip_http
    pico_lwip_nosys
)

# Add include directory for lwipopts.h
target_include_directories(dezkvm_pico PRIVATE src)

# Ensure USB output, disable UART output
pico_enable_stdio_usb(dezkvm_pico 1)
pico_enable_stdio_uart(dezkvm_pico 0)

# Generate map/bin/hex/uf2 files
pico_add_extra_outputs(dezkvm_pico)
