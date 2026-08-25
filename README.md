# DezKVM-Go Pico Webserver

This repository provides an automated compilation of the [DezKVM-Go](https://github.com/tobychui/DezKVM-Go) Web UI for the Raspberry Pi Pico microcontroller family (RP2040 and RP2350). 

**Important Note:** This project's sole purpose is to automatically package and compile the upstream web interface so that it can be hosted locally, directly from the Pico's flash memory and over USB-Ethernet. This allows the KVM software to run completely offline without requiring an internet connection.

## Acknowledgements & Upstream Project

Thanks to TobyChui for creating the original [DezKVM-Go](https://github.com/tobychui/DezKVM-Go) project. 

If you are interested in a dedicated hardware KVM solution, please refer to his original project, the hardware designs, and the upstream repository.

## Features
- Fully automated builds via GitHub Actions
- Pre-compiled `.uf2` firmware releases for:
  - Raspberry Pi Pico / Pico W (RP2040)
  - Raspberry Pi Pico 2 / Pico 2 W (RP2350 ARM Cortex-M33)
  - Raspberry Pi Pico 2 / Pico 2 W (RP2350 Hazard3 RISC-V)

  <small>*(Note: The ARM and RISC-V builds for the Pico 2 are functionally identical. The RP2350 has dual-architecture cores, so you can simply pick whichever architecture you prefer to run.)*</small>

- Runs completely offline, hosting the DezKVM-Go UI directly from the Pico's flash memory.

## Building from Source

To compile the firmware yourself:
1. Ensure you have the [Raspberry Pi Pico SDK](https://github.com/raspberrypi/pico-sdk) installed and configured.
2. Clone this repository.
3. Run `python3 scripts/bundler.py` to fetch and package the web assets from the upstream repo into `src/html_data.h`.
4. Use standard CMake build steps to compile.

## Installation & Usage

### Flashing the Firmware
1. Download the appropriate `.uf2` file for your hardware from the [Releases](../../releases) page.
2. Hold down the **BOOTSEL** button on your Raspberry Pi Pico.
3. While holding the button, plug the Pico into your computer via USB.
4. A new mass storage drive named `RPI-RP2` will appear.
5. Drag and drop the `.uf2` file onto the `RPI-RP2` drive. The Pico will automatically flash and reboot.

### Accessing the Web Interface
1. Once rebooted, the Pico will enumerate on your computer as a USB Network Adapter (RNDIS / CDC-NCM).
2. Wait a few moments for your operating system to recognize the adapter.
3. Open a Chromium-based web browser (Chrome, Edge, etc.) and navigate to `https://192.168.7.1`.
4. The DezKVM-Go web interface will load directly from the Pico's memory!

## Hardware Wiring (DezKVM-Go PCB)

To use this Pico webserver alongside the DezKVM-Go hardware using a single upstream USB cable, you can wire the Pico directly to the DezKVM-Go internal USB hub header *(Note: The internal USB header is available on the v2 PCB revision)*. There are two recommended methods to achieve this:

**Method 1: Stripped Micro-USB Cable (Easiest)**
1. Plug a standard Micro-USB cable into the Raspberry Pi Pico.
2. Cut the other end of the cable and strip the 4 internal wires.
3. Solder the stripped wires to the DezKVM-Go internal header:
   - **Red Wire (5V)** -> DezKVM-Go `VCC / 5V`
   - **White Wire (D-)** -> DezKVM-Go `DM`
   - **Green Wire (D+)** -> DezKVM-Go `DP`
   - **Black Wire (GND)** -> DezKVM-Go `GND`

*(Note: USB wire colors are typically Red/White/Green/Black as listed above, but this can vary depending on the cable manufacturer. Use a multimeter to verify if you are unsure.)*

**Method 2: Direct Soldering to Pico Pads (Cleaner)**
For a more permanent and compact installation, you can solder wires directly to the Pico's pins and test pads on the back of the board:
- **VBUS (Pin 40)** -> DezKVM-Go `VCC / 5V`
- **TP2 (Test Pad on back, D-)** -> DezKVM-Go `DM`
- **TP3 (Test Pad on back, D+)** -> DezKVM-Go `DP`
- **GND (Pin 38 or any GND)** -> DezKVM-Go `GND`

*(Note: Please verify the exact pinout order on your specific DezKVM-Go PCB revision before applying power, as header layouts can vary.)*

## License

This project, as a hardware port and derivative work of DezKVM-Go, is licensed under the **GNU General Public License v3.0**. See the `LICENSE` file for more details. All web interface assets (HTML, CSS, JS, Images) remain under the copyright and licensing of their original authors.
