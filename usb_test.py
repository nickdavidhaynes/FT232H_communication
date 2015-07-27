'''
Test program for reading and writing bytes between the PC and the FT232H
USB chip.

Note: For this script to work, you must have the FTDI D2XX drivers 
(http://www.ftdichip.com/Drivers/D2XX.htm) and the d2xx python wrapper
(http://www.imaginaryindustries.com/blog/?p=224) installed.

Also depends on Tkinter for creating a GUI.
'''


from Tkinter import *
import d2xx

# list devices by description, returns tuple of attached devices description strings
d = d2xx.listDevices(d2xx.OPEN_BY_DESCRIPTION)
print d

# open device
h = d2xx.open(0)

# set RX/TX timeouts
h.setTimeouts(1000,1000)

class Application(Frame):
	def read_byte(self):
		h.purge()
		bytes_waiting = h.getQueueStatus()
		data = h.read(5)
		print ord(data)
		print bytes_waiting


	def createWidgets(self):
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["fg"]   = "red"
		self.QUIT["command"] =  self.quit

		self.QUIT.pack({"side": "left"})

		self.hi_there = Button(self)
		self.hi_there["text"] = "Read data",
		self.hi_there["command"] = self.read_byte

		self.hi_there.pack({"side": "left"})

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()




# write a byte
h.write(chr(4))
'''
# read some bytes
bytes_waiting = h.getQueueStatus()
print bytes_waiting
data = h.read(bytes_waiting)
print ord(data[0])
'''

# close device
h.close()

