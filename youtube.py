# takes the first video link from the search query
# uses chrome/chromium to play it

import indepFunc as ip
import conRecog as cr
import urllib
import urllib2
import os
from bs4 import BeautifulSoup
from termcolor import colored
import time

# different versions of victoria recognized frequently
triggerList = ["victoria","victorious","pictorial","victoriya","call victoria","pretoria","vicktoria"]

# controls available while the video is playing
videoControls = ["play","stop","pause","volume up","volume down"]

# keypresses used to implement video controls
fullScreen_sequence = '''keydown F
keyup F
'''

stop_sequence = '''keydown Control_L
key W
keyup Control_L
'''

pause_sequence = '''keydown K
keyup K
'''

volume_down_sequence = '''keydown Down
keyup Down
'''

volume_up_sequence = '''keydown Up
keyup Up
'''

# function to open tab in the browser, if text is to be searched is available
def play(textToSearch,device):
	# web scrap and find the video urls from code

	query = urllib.quote(textToSearch)

	# form the search query
	url = "https://www.youtube.com/results?search_query=" + query
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html,"html.parser")

	# search for the tags with url links
	urlList = []
	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
	    u = 'https://www.youtube.com' + vid['href']
	    urlList.append(u)

	# 'mplayer "$(youtube-dl -g [url])"
	# youtube-dl dependency, updates frequently

	# command = "mplayer -fs '$(youtube-dl -g " +urlList[1]+ ")'"
	# command1 = 'gnome-terminal --command="'+command+'"'
	# print(command1)
	# os.system(command1)

	# play the top link found
	if(device==1):
		command = "google-chrome "+urlList[1]
		command1 = 'gnome-terminal --command="'+command+'"'
	else:
		command = "chromium-browser "+urlList[1]
		command1 = 'lxterminal --command="'+command+'"'
	# print colored("\n"+command1+"\n",'yellow')
	os.system(command1)

# function to open tab in the browser, if link is available
def playLink(link,device):
	if(device==1):
		command = "google-chrome -incognito"+link
		command1 = 'gnome-terminal --command="'+command+'"'
	else:
		command = "chromium-browser -incognito"+link
		command1 = 'lxterminal --command="'+command+'"'
	# print colored("\n"+command1+"\n",'yellow')
	os.system(command1)

# driver function
def youtube(textToSearch,flag,device):
	# flag=0 if link is available, flag=1 if text is to be searched
	if(flag==0):
		play(textToSearch,device)
	elif(flag==1):
		playLink(textToSearch,device)

	# videoPlaying is a flag to keep track if the video is playing
	videoPlaying = True
	
	# countyt keeps track of browser PIDs running in background
	# countyt=1 when the browser is not running
	countyt = 0
	
	while(countyt!=1):
		
		if(countyt==0): # <- runs only first time
			# wait for 5 seconds, so that video starts playing
			time.sleep(15)
			# then press F to enter full-screen mode
			ip.keypress(fullScreen_sequence)
		
		countyt = 0
		# read how many lines are there with "browser" in background running
		# around 7-8 when browser is running
		if(device==1):	p = os.popen("ps ux | grep chrome","r")
		else:	p = os.popen("ps ux | grep chromium","r")
		while(True):
			line = (p.readline()).strip()
			if not line: break
			countyt+=1

		# at this point, video is playing in browser in fullscreen mode
		# program is listening in background

		print colored("\nSay 'Victoria' access video controls!\n",'green')
		audio = ip.recordAudio(device);
		
		if(cr.isConnected()):
			if(device==1):	outText = cr.googleRecog(audio)
			else:	outText = cr.bingRecog(audio)[0]
		else: outText = cr.sphinxRecog(audio)

		# if text is not understood, continue listening
		if(outText==-1):
			continue

		# if text is understood
		else:
			# check if victoria is said
			if((outText.lower() in triggerList)or("victoria" in outText.lower())):
				# enters if text was victoria
				if(videoPlaying==True):
				# pause the video	
					ip.keypress(pause_sequence)
					videoPlaying = False
				ip.play("Which control sequence?")
				while(1):
					print colored("\nOptions available :",'yellow')
					print colored(videoControls,'yellow')
					print("\n")

					# record which video control has to be accessed
					audio = ip.recordAudio(device)
					if(cr.isConnected()): outText = cr.bingRecog(audio)[0]
					else: outText = cr.sphinxRecog(audio)

					# if above text is not recognized, ask again
					if(outText==-1):
						print colored("\nNot a control, try again!\n",'red')
						ip.play("Not a control, try again!")

					elif(outText.lower() in videoControls):
						# enter if text is a videoControl
						# convert text to lower for easier comparison
						text = outText.lower()
						if(text=="pause"):
							break

						# close the browser window as stop sequence
						elif(text=="stop"):
							ip.keypress(stop_sequence)
							time.sleep(1)
							return True
						
						elif(text=="play"):
							if(videoPlaying!=True):
								ip.keypress(pause_sequence)
								videoPlaying = True
								break
							else:
								print colored("\nVideo is already playing!\n",'red')
								break
						
						# for volume controls, press the concerned key 3 times
						# each with 1 second pause
						elif(text=="volume up"):
							for i in range(3):
								ip.keypress(volume_up_sequence)
								time.sleep(1)
							ip.keypress(pause_sequence)
							videoPlaying = True
							break
						
						elif(text=="volume down"):
							for i in range(3):
								ip.keypress(volume_down_sequence)
								time.sleep(1)
							ip.keypress(pause_sequence)
							videoPlaying = True
							break

					# if text is "exit", play video and stop listening
					elif(outText in ["exit","Exit","exact","Exact"]):
						print colored("\nExiting..\n",'red')
						ip.play("Exiting")
						ip.keypress(pause_sequence)
						videoPlaying = True
						break

			# if text is recognized but it is not victoria, continue listening
			else:
				continue

	return
