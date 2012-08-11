RaspberryPiSDSetup
==================

Tool to easily setup an SD Card into a bootable Raspberry Pi drive. 
==Requires an empty SD Card==

#Description 

This is meant to grab or use an existing linux image and setup formant an SDCard into a bootable Linux image preconfigured for Raspberry Pi.
Should help saving some time in configuring a Raspberry pi


IMPORTANT: read carefully, and note which volume will be formatted. 
This tool will try to prevent you from shooting yourself in the foot but in any case, selecting the wrong volume could result in formatting
an unwated drive and loosing its data. 


#Usage
- Insert an SD Card 
- run <tt>python setuprbpi.py default </tt>
- Choose the SDCard volume and 
- wait for it...

Or...

- Download your RBPi image of your choice
- run <tt>python setuprbpi.py <path_to_unzipped_image_file> </tt> and
- wait for it...


#FAQ 

- How do I know which volume is the SD Card?

  Open Finder and in you device List, the SD card should have a name ie. <tt>Kingston</tt>. the SD card will show up in the list as <tt>/Volumes/Kingston</tt>
  Otherwise, Open Disk Utility and find your SD card. You can change its name here. 
  
- Should the SD be empty?

  No. But double check you don't loose something, the format will wipe out the SD card contents.
  
- It's all done, now what?
  
  Insert your SD card into the Raspberry Pi and turn it On. Enjoy!

- Can I modify the files once the image is written?
  Yes! but the image (unless it's a custom image) will create 2 shares on the SD. one of them will be a linux EXT partition
  you'll need to install :
  
  - MacFuse - https://code.google.com/p/macfuse/

  - Fue-Ext2 - http://sourceforge.net/projects/fuse-ext2/

- Why id <tt> default </tt> downloading this huge file?
  It is downloading the base preconfigured image file. It's around 500MB (Just to take in consideration, in case you are tethering or still on AOL dialing up)

- Will copying the image to the SD Card take too long?
  Yes. Expanding to the SD takes a while, could take several minutes. On the bright side: This is the perfect moment to brew a Legendary Cup of Coffee
  