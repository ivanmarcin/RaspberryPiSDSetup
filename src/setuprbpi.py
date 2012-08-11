
#============================= 
#   * Raspberry Pi SDCard imager
#   * Ivan Marcin
#   * 2012
#=============================
#
# Copyright Ivan Marcin  2012
# The following code is licenced under the Gnu Public Licence, please see gpl.txt for reference
#  This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import re, os, urllib2, time, sys, threading
import terminal 
import ansi

from commands import *
from sys import exit
from subprocess import call


#For the colored output.
screen = terminal.get_terminal()

#path to the preconfigured image
remoteImagePath = "http://files.velocix.com/c1410/images/raspbian/2012-07-15-wheezy-raspbian/2012-07-15-wheezy-raspbian.zip"
raspberryPiImageFileName = "2012-07-15-wheezy-raspbian.zip"

#Wrapper method to shorter color changes
def Color(theColor) :
	"""
	Sets the foreground color of the terminal text.
	Any following prints will be of this color.
	"""
	screen.set_color(terminal.colors[theColor])
	pass

def GetSdDeviceList() :
	"""
	Performs the system call DF -H 
	and returns a dictionary of the possible volumes 
	to use as a destination.
	"""
	devicelist = dict()
	#Get the device list from DF -H
	df = getoutput('df -h').split('\n')

	#split the data per line minus the header
	for x in xrange(1, len(df)):
		line = df[x].split()

		#remove known entries which may screw things up. like root mount
		if (line[8] != '/' and line[8] != '100%' and line[0] !='devfs' and line[0] != 'map'):
			devicelist[x] = [line[0] , line[8], line[8].split('/')[-1]]
			#print devicelist[x]
	return devicelist


def GetDdCompatibleDeviceName(device):
	"""
	The device name needs to be parsed into a valid Disk mount format 
	OSX DD has a funky way of naming the drives so instead of using 
	the std path like /Dev/disk0s1
	it appends an R and the disk number to disk ,ie: rdisk1
	"""
	dev =  'r' + device[0].split('/')[-1][:-2]
		
	if( dev[:5] != "rdisk" or not dev[-1:].isdigit()) :
		Color("RED")
		print "It appears the name for the device selected can't be parsed into a valid Disk ID"
		print "The device isn't an SD . Please rerun the script and use a different Volume"
		Color("CYAN")
		print "Example of a Valid Name: [rdisk1] 	Parsed Name: [%s]" % ( dev)
		sys.exit(-1)

			
	##Replace the volume path with the X friendl device name
	device[1] = dev
	
	return device


def GetSdDeviceName() :
	devices = GetSdDeviceList()
	deviceSelected = ''

	while (deviceSelected == ''):
		Color("WHITE")
		print ('====================================================================================================')
		print 'This Are the available Volumes in your system. pick the volumen of the SDCard to be formatted' 
		print ('____________________________________________________________________________________________________')

		for x in devices:

			Color("RED")			
			sys.stdout.write( 'Vol # [%d]: \t ' % (x) )

			Color("BLUE")			
			sys.stdout.write( 'Device Name: \t ' )

			Color("GREEN")
			sys.stdout.write( devices[x][2] )

			Color("BLUE") 
			sys.stdout.write( '\t \t \t Mount Point: \t' )

			Color("GREEN")
			sys.stdout.write( devices[x][0] )

			Color("WHITE")
			
			print '\n_________________________________________________________________________________________________'

		print 'Type in the number indicating the volume to continue '
		selection = raw_input()
		print '\n'
		if (devices.has_key(int(selection))):
			print 'Device Selected: %s\n' % ( devices[int(selection)])
			deviceSelected = devices[int(selection)]
		else:
			Color("RED")
			print '%s is an invalid selection. Please select a valid volume number or CTRL+C to quit\n' % (selection)

	return deviceSelected


def UnmountSdCard(mountPath):
	"""
	Unmounts the device in order to deploy the image into the disk 
	"""
	Color("BLUE")
	print "Unmounting the device. Please type password if requests[in case of not running as root]"
	output = getoutput("sudo diskutil unmount %s" % (mountPath))
	Color("YELLOW")
	print  output
	Color("WHITE")

def RawCopyImageToSd(imageFile, deviceName):

	Color("GREEN")
	print "Copying %s into %s. please wait since this might take a while..." % (imageFile,deviceName)

	command = "sudo dd bs=1m if=%s of=/dev/%s" % (imageFile, deviceName)

	print "Executing : %s" % (command)
	output = getoutput(command)

	if( "Resource busy" in output) :
		Color("RED")
		print "There's more than one partition on the SD Card. unmount or rerun script"		
		print output
		sys.exit(-1)
	else:
		Color("BLUE")
		print output

def GrabImage(fileName):
	
	if (fileName == 'default'):
		Color("YELLOW")	
		print "DEFAULT was selected. The default image will be downloaded"

		Color("GREEN")

		call(["wget", remoteImagePath] )
		
		Color("BROWN")
		call(["unzip", "-o",raspberryPiImageFileName] )
		
		fileName = "./" + raspberryPiImageFileName[:-3] + "img"
		#fileName = './raspberrypi-fedora-remix-14-r1.img'

	Color("WHITE")	
	if( not os.path.exists(fileName)):
		Color("RED")
		print "The image file selected does not exist: %s" % (fileName)
		sys.exit(-3)
	else:
		return fileName


def SetupPi(imageParam):
	"""
	Do the magic. Setup RaspberryPi into the SDCard
	"""

	ImageFile = GrabImage(imageParam)
	SDCard = GetSdDeviceName()
	SDCard = GetDdCompatibleDeviceName(SDCard)

	UnmountSdCard(SDCard[0])
	RawCopyImageToSd(ImageFile, SDCard[1])

	Color("YELLOW")
	print "\nAll done!"
	Color("BLUE")
	print "Plug the SD card into your RaspberryPi and enjoy!"
	pass


###Instructions###
def Printinstructions():
	"""
	Prints the instructions and welcome to the screen
	"""

	Color ("PURPLE")
	print ('\n=================Raspberry Pi SDCard setup=================\n')

	Color("GREEN")
	print """   .~~.   .~~.
  '. \ ' ' / .'"""

  	Color("RED")
  	print """   .~ .~~~..~.
  : .~.'~'.~. :
 ~ (   ) (   ) ~
( : '~'.~.'~' : )
 ~ .~ (   ) ~. ~
  (  : '~' :  ) Raspberry Pi
   '~ .~~~. ~'
       '~'' """

	screen.set_color(terminal.colors["BLUE"])
	print """\n\n\
	Welcome!

	This utility (V1) will format, and setup an empty SD Card 
	with a linux image ready to boot into raspberry pi.

	usage: 
		python	setuprbpi <imageFile | default>

	imageFile:  
		Option 1: 
			The path to the file containing the linux image.
			This should be the unzipped .img file.
			One can be obtained from http://www.raspberrypi.org/downloads  
				
		Option 2: 
			type 'default'
			will download a preconfigure image (~500mb download) for you
			and use it write the SD Card
	"""
	
	pass

if __name__ == '__main__' :
	Printinstructions()

	if(len(sys.argv) != 2):
		Color("RED")
		print "Invalid Arguments"
		sys.exit(1)
	
	if os.uname()[0] != 'Darwin':
		screen.set_color(terminal.colors["RED"]);
		print "Sorry! This only works on OSX for now. Exiting..."
	else:
		SetupPi(sys.argv[1])
