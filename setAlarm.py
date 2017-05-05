from termcolor import colored
import time
import os
import sys

# read the number of seconds provided as cl agrument
seconds = int(sys.argv[1])
# read the time provided as cl agrument
t = str(sys.argv[2])
# read the device id provided as cl agrument
device = int(sys.argv[3])

print colored("Alarm set for : "+t,'yellow')

time.sleep(seconds)

# change the directory and play mp3
if(device==1):	os.chdir("/home/piyush/final")
else:	os.chdir("/home/pi/final")

os.system("mplayer alarm.mp3")