# "python main.py" to run
# refer requirements file before running project

import indepFunc as ip
import phraseRecog as pr
import conRecog as cr
import speech_recognition as sr
from termcolor import colored

device = 0
while(device not in [1,2]):
	print("Linux Laptop : 1")
	print("Raspberry Pi : 2")
	device = int(input("Enter the device id - "))
	print("\n")

r = sr.Recognizer()
# reset energy threshold according to the ambient noise
r.dynamic_energy_threshold = True
# silent time considered as end of the phrase
# r.pause_threshold = 0.5

print colored("\nAdjusting for ambient noise!\n",'yellow')
with sr.Microphone() as source: r.adjust_for_ambient_noise(source, duration = 2)

# updates movies, music and photos is file system
ip.updateDirect(device)

# phrases often recognized when saying victoria
triggerList = ["victoria","victorious","pictorial","victoriya","call victoria","pretoria","vicktoria"]

while(True):
	print colored("\nSay 'Victoria' to wake me up!\n",'yellow')
	audio = ip.recordAudio(device);
	
	if(cr.isConnected()): 
		if(device==1):	outText = cr.googleRecog(audio)
		else:	outText = cr.bingRecog(audio)[0]
	else: outText = cr.sphinxRecog(audio)

	if(outText==-1):
		# if text is not recognized, continue listening
		continue
	elif(outText in ["exit","Exit","exact","Exact"]):
		# exit the whole script
		print colored("\nEnding Session..\n",'red')
		ip.play("Ending Session")	
		break
	else:
		# if Victoria is said, proceed to phraseRecog function
		if(outText.lower() in triggerList):
			pr.phraseRecog(device)
		elif("victoria" in outText.lower()):
			pr.phraseRecog(device)
