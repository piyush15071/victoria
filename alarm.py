# Functions : set

from datetime import *
from termcolor import colored
from time import gmtime, strftime
import time
import os
import indepFunc as ip

def set(hour,minutes,ampm,device):
	localtime = time.localtime(time.time())	# current time

	# e.g, 08:21 PM <- line below creates string in this format for alarm time
	time12hourformat = hour+":"+minutes+" "+ampm.upper() 
	
	# convert alarm time from 12hr format to 24hr
	t2 = (str(datetime.strptime(time12hourformat, '%I:%M %p')).split(" ")[1])[:5]
	
	# current time in 24hr format
	t1 = str(localtime.tm_hour)+":"+str(localtime.tm_min)
	
	FMT = '%H:%M' # <- we just need hours and minutes

	# difference between both times, in number of days, hours and minutes
	tdelta = str(datetime.strptime(t2, FMT) - datetime.strptime(t1, FMT))

	# below lines are for extracting hours and minutes
	if(len(tdelta.split(","))==2):
		tdelta = (tdelta.split(",")[1]).strip(" ")
	parts = tdelta.split(":")

	# calculate seconds from minutes and hours
	totalSeconds = (int(parts[0])*3600)+(int(parts[1])*60)

	# open a separate terminal which will play the mp3 file after n tdelta seconds
	# and return to main function
	if(device==1):
		command = "'python /home/piyush/final/setAlarm.py "+str(totalSeconds)+" "+str(hour)+":"+str(minutes)+str(ampm.upper())+" "+str(device)+"'"
		os.system("gnome-terminal --command "+command)
	else:
		command = "'python /home/pi/final/setAlarm.py "+str(totalSeconds)+" "+str(hour)+":"+str(minutes)+str(ampm.upper())+" "+str(device)+"'"
		os.system("lxterminal --command "+command)

	print colored("\nAlarm set!\n",'green')
	ip.play("Alarm set!")