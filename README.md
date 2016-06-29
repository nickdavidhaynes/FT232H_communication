# FT232H_communication

Contents
- What's included
- Important information
- Getting started (Windows)
- Using USB.v in your Verilog project
- Using the USB_blackbox Quartus project to test your USB comms

## What's included

1. The black box Verilog module, called USB.v that handles all
communication with the FTDI FT232H USB chip
2. A Quartus project file for verifying that your USB communication is 
working properly
3. LabVIEW files to accompany the Quartus project

## Important information

- This code is intended to communicate with the FT232H USB chips in asynch
245 FIFO mode. Max speed is 8 x 1 Mb/s.
- Make sure you have the FTDI D2XX drivers installed on your computer.
- The Quartus files are intended for use with the DE2-115 dev board.

# Getting started (Windows)

Before using the USB module, you'll need to do a few things:
1. Install the FT D2XX drivers
2. Download the FT_Prog program
3. If using Python, download the python USB wrapper

1. Install the FT D2XX drivers 
These drivers allow your computer to communicate with the USB chip.  Download the most current file from 
http://www.ftdichip.com/Drivers/D2XX.htm and run the .exe. To verify drivers are successfully installed, plug the USB chip into your computer and navigate to Control Panel -> Device Manager. Expand the 'Universal Serial Bus controllers' tree. 'USB Serial Converter' should be listed. Double click it, and navigate to the Details tab. Select 'Bus reported device description' from the pull-down menu. The value field should say 'UM232H-B'. If not, something is wrong.

2. Download the FT_Prog program
THIS STEP IS ONLY NECESSARY THE FIRST TIME YOU USE A NEW CHIP (if you're
unsure, follow these steps anyway). These chips are able to operate with several different protocols (see
device documentation for more info). The protocol we use here is called asynch 245 FIFO. The FT Prog utility allows the user to set the chip to operate with this protocol. Download FT Prog from http://www.ftdichip.com/Support/Utilities.htm and
run the installer. Connect the USB chip to the PC and run FT Prog. Click the magnifying glass in the tool bar to tell the program to scan the USB ports for connected devices. The program will find the USB chip ('Chip Type' will say 'FT232H') Under FT EEPROM -> Hardware Specific -> Hardware, click the button to select '245 FIFO'. Verify that under FT EEPROM -> Hardware Specific -> Driver, 'D2XX Direct' is selected. Program the chip by clicking the lightning bolt in the toolbar, then clicking 'Program' in the pop-up window

3. If using Python, download the Python USB wrapper 
*UPDATE: The link provided is dead. Currently working on finding an alternate solution.*

The FTDI D2XX drivers that you installed in step 1 above don't natively work with Python. To get them to work, we need a 'wrapper' that translates commands given in Python to something the drivers understand (i.e. C code). First, check your version of Python. USB communication only works with Python 2. If you have Python 3, you'll have to download and use Python 2.7. Download the wrapper from http://www.imaginaryindustries.com/blog/?p=224 . You want the win32 version. You can now use the D2XX drivers by putting the command 'import d2xx as...' in your Python code.

## Using USB.v in your Verilog project

USB.v is meant to be a black box module for USB I/O. It handles everything
necessary for using the FT232H to send and receive data between the
computer and the DE2-115. Include it in your Quartus project to use USB
communication.

The ports are:
USB(CLOCK_50, GPIO, write_request, byte_received, write_data, read_data)

Inputs:
CLOCK_50 - 50 MHz clock
[7:0] write_data - the 8 bits of data you would like to write to the PC
reset - when high, communication is reset.
write_request - Pulse high when you are ready to send write_data to the PC

Inouts:
[35:0] GPIO - The 36 GPIO pins on the DE2-115

Outputs:
[7:0] read_data - the 8 bits of data that are read from the PC
byte_received - Goes high to let you know when a byte is received from the PC

## Using the USB_blackbox Quartus project to test your USB comms

The Quartus project is designed to make sure the USB communications are
working properly. The byte spelled out by the LabVIEW switches is
periodically sent to the FPGA and displayed on its green LEDs. At the same
time, the byte spelled out on the FPGA switches is periodically sent to
the PC and displayed on the green LabVIEW LEDs. If everything is working
properly, these switches and LEDs should operate completely independently
from each other.
