# FT232H_communication

This repo contains everything you need to get started sending data between an FPGA connected to a FTDI FT232H USB chip and an external computer using Python and Verilog. These instructions are somewhat specific to having the FT232H connected to the GPIOs of an Altera DE2-115 board, but could be generalized to other devices.

## Getting started (Windows)

### Install the FT D2XX drivers

These drivers allow your operating system to communicate with the USB chip. Download the most current file from http://www.ftdichip.com/Drivers/D2XX.htm and run the .exe. To verify drivers are successfully installed, plug the USB chip into your computer and navigate to Control Panel -> Device Manager. Expand the 'Universal Serial Bus controllers' tree. 'USB Serial Converter' should be listed. Double click it, and navigate to the Details tab. Select 'Bus reported device description' from the pull-down menu. The value field should say 'UM232HB'. If not, something is wrong.

### Download the Python wrapper to D2XX
Unfortunately, FTDI does not provide an official library for interacting with the D2XX driver from Python. Instead, we'll use a wrapper.

First, make sure that the computer you're using is running Python 2.7.x (if you're a Python pro, 3.x should be fine as well). From the console, running

`python --version`

will print the default version of Python. If you're not on 2.7, consider using the Anaconda (https://www.continuum.io/downloads) distribution - Anaconda vastly improves Python packaging on Windows.

If you don't already have pip installed (pip comes with Anaconda, but may not come with other distributions), follow the instructions here to get it - https://pip.pypa.io/en/stable/installing/.

Finally, we can download and install the D2XX wrapper by running

`pip install ftd2xx`

from the console. You should see some text printed to the screen, with a message telling you that the installation was successful.

### Configure the chip
Note that this step is only necessary the first time you use a brand-new chip.

One of the nice things about the FT232H chips is that they are capable of operating with a number of different I/O protocols (see http://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT232H.pdf for more details). The protocol we use here is called asynch 245 FIFO. By default, a brand-new chip will not be configured for asynch 245 FIFO, but we can use the free FT Prog utility to reconfigure it.

Download FT Prog from http://www.ftdichip.com/Support/Utilities.htm and run the installer. Connect the USB chip to the PC and run FT Prog. Click the magnifying glass in the tool bar to tell the program to scan the USB ports for connected devices. The program will find the USB chip ('Chip Type' will say 'FT232H') Under FT EEPROM -> Hardware Specific -> Hardware, click the button to select '245 FIFO'. Verify that under FT EEPROM -> Hardware Specific -> Driver, 'D2XX Direct' is selected. Program the chip by clicking the lightning bolt in the toolbar, then clicking 'Program' in the pop-up window.

## Getting started (OS X/MacOS and Linux)

### Install the FT D2XX drivers 
These drivers allow your operating system to communicate with the USB chip. Download the most current file from http://www.ftdichip.com/Drivers/D2XX.htm.

### Download the Python wrapper to D2XX
Unfortunately, FTDI does not provide an official library for interacting with the D2XX driver from Python. Instead, we'll use a wrapper.

First, make sure that the computer you're using is running Python 2.7.x (if you're a Python pro, 3.x should be fine as well). From the terminal, running

`python --version`

will print the default version of Python. If you're on 2.6 or lower, consider upgrading.

If you don't already have pip installed (running `which pip` doesn't print anything), follow the instructions here to get it - https://pip.pypa.io/en/stable/installing/.

Finally, we can download and install the D2XX wrapper by running

`pip install ftd2xx`

from the console. You should see some text printed to the screen, with a message telling you that the installation was successful.

### Configure the chip
Note that this step is only necessary the first time you use a brand-new chip.

One of the nice things about the FT232H chips is that they are capable of operating with a number of different I/O protocols (see http://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT232H.pdf for more details). The protocol we use here is called asynch 245 FIFO. By default, a brand-new chip will not be configured for asynch 245 FIFO, but we can use the free FT Prog utility to reconfigure it.

Unfortunately, FT Prog will only run on Windows. Find a friend who's willing to help you out and follow step 3 in the Windows installation instructions.

## Testing that everything works

To verify the installation worked correctly, there is some sample Verilog and Python included in this directory.

Create a new project in Quartus and include the three `.v` files located in this repo. Make sure to connect the declared ports to the correct pins on your FPGA and compile the design. After connecting the FT232H to the computer, program the FPGA and run

`python test_usb.py`

from the project directory. You should see a prompt asking for input. By typing `GET`, the computer will fetch a byte from the FPGA. Try using switches 0-7 on the DE2-115 board to enter a binary integer, and oberve that the base-10 representation of that integer is printed to the screen.

If you type an integer (0-255) into the prompt, that integer is written to the FT232H and received by the FPGA, where it is displayed in base-2 on the 8 green LEDs.

Enter `EXIT` to leave the prompt.

## Using USB.v in your Verilog project

`USB.v` is meant to be a black box module for USB I/O. It handles everything
necessary for using the FT232H to send and receive data between the
computer and the DE2-115. Include it in your Quartus project to use USB
communication.

The ports are:
USB(CLOCK_50, GPIO, write_request, byte_received, write_data, read_data)

### Inputs:
* CLOCK_50: a 50 MHz clock
* [7:0] write_data: the 8 bits of data you would like to write to the PC
* reset: when high, communication is reset.
* write_request: Pulse high then low to transfer write_data from the FPGA pins to the FT232H.

### Inouts:
* [35:0] GPIO - The 36 GPIO pins on the DE2-115

### Outputs:
* [7:0] read_data - the 8 bits of data that are read from the PC
* byte_received - Goes high when data is available waiting to be read onto the FPGA.

