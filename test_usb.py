import ftd2xx as d2xx

while True:
    num_input = raw_input('Enter an integer, GET, or EXIT: ')

    if num_input == 'EXIT':
        break

    # These 3 lines of boilerplate are necessary each time you open the device
    usb = d2xx.open(0)
    usb.setTimeouts(100, 100)
    usb.setUSBParameters(640)

    if num_input == 'GET':
        bytes_received = usb.getQueueStatus()
        try:
            data = usb.read(bytes_received)
            print ord(data[1])
        except IndexError:
            print 'No bytes in the transmit queue'
    else:
        try:
            num_int = int(num_input)
        except ValueError:
            print 'Error: To write to device, enter an integer between 0 and 255. Otherwise, enter GET to read from the device or EXIT to quit.'
            usb.close()
            continue
        if num_int < 0 or num_int > 255:
            print 'Error: Enter an integer between 0 and 255'
            usb.close()
            continue
        usb.write(chr(num_int))

    usb.close()
