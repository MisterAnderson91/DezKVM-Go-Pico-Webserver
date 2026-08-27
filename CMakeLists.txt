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
    src/usb_descriptors.c
    src/fs.c
    ${PICO_SDK_PATH}/lib/tinyusb/lib/networking/dhserver.c
    ${PICO_SDK_PATH}/lib/tinyusb/lib/networking/dnserver.c
    ${PICO_SDK_PATH}/lib/tinyusb/lib/networking/rndis_reports.c
)

# Pull in our pico_stdlib and tinyusb network/lwip/mbedtls dependencies
target_link_libraries(dezkvm_pico
    pico_stdlib
    hardware_pwm
    tinyusb_device
    tinyusb_board
    pico_lwip_nosys
    pico_lwip_http
    pico_mbedtls
    pico_lwip_mbedtls
)

if (TARGET pico_cyw43_arch_none)
    target_link_libraries(dezkvm_pico pico_cyw43_arch_none)
endif()

# Add include directories
target_include_directories(dezkvm_pico PRIVATE
    src
    ${PICO_SDK_PATH}/lib/tinyusb/lib/networking
)

# Add compile definitions
target_compile_definitions(dezkvm_pico PRIVATE
    NO_SYS=1
)

# Ensure USB output, disable UART output
pico_enable_stdio_usb(dezkvm_pico 1)
pico_enable_stdio_uart(dezkvm_pico 0)

# Generate map/bin/hex/uf2 files
pico_add_extra_outputs(dezkvm_pico)
