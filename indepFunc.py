# Functions : createmp3, play, updateDirect, recordAudio, keypress

from subprocess import Popen, PIPE
from termcolor import colored
import speech_recognition as sr
import time
import led
import os

r = sr.Recognizer()

def createmp3(text):
	# HTTPSConnectionPool <- frequently occuring error
	# create an mp3 file from given text using google text to speech cli utility
	text = text.encode(encoding='UTF-8',errors='strict')
	command = "gtts-cli.py " + "\"" + text + "\"" + " -l 'en' -o temp.mp3"
	# print colored("\n"+command+"\n",'yellow')
	os.system(command)

def play(text):
	# lines below mp3 files are created
	# needed because gtts fails at times, hence no mp3 file is created
	files = []
	while("temp.mp3" not in files):
		createmp3(text)
		time.sleep(1)
		p = os.popen('ls',"r")
		files = []
		while(True):
			line = (p.readline()).strip()
			if not line: break
			files.append(line)

	# play the mp3 file
	os.system("mplayer temp.mp3 > /dev/null 2>&1")
	# remove the mp3 file after playing
	os.system("rm temp.mp3")

def updateDirect(device):
	# change the directory in sub-process
	if(device==1):	os.chdir('/home/piyush/ied')
	else:	os.chdir('/home/pi/ied')
	# read all files into a python list
	p = os.popen('ls',"r")
	direcs = []
	while(True):
		line = (p.readline()).strip()
		if not line: break
		direcs.append(line)
	print colored("\ndirecs : ",'yellow')
	print colored(direcs,'yellow')
	print "\n"
	
	# loop in every directory available and update out.txt file
	for i in direcs:
		if(i=="temp.mp3"):	os.system("rm temp.mp3")
		else:
			try:
				os.chdir(i)
			except:
				continue
			p = os.popen('ls',"r")
			files = []
			while(True):
				line = (p.readline()).strip()
				if not line: break
				# do not include out.txt file
				if(line[len(line)-3:len(line)]!='txt'):
					files.append(line)
			# write file names to out.txt
			ff = open("out.txt",'w')
			for k in files:
				ff.write(k+'\n')
			# close the file object
			ff.close()
			os.chdir('..')

def recordAudio(device):
        if(device!=1):  led.on()
	print colored("\n**start record**\n",'magenta')
	# only records for 5 second, as hardcoded value
	with sr.Microphone() as source: audio = r.record(source, duration=5)
	print colored("\n**end record**\n",'magenta')
	if(device!=1):  led.off()
	return audio

def keypress(sequence):
	# function for communicating keypress sequence to standard input
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence)
