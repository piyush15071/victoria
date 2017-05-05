# Functions : isConnected, bingRecog, googleRecog, sphinxRecog

from termcolor import colored
import socket
import json
import speech_recognition as sr
import indepFunc as ip
import time

r = sr.Recognizer()
REMOTE_SERVER = "www.google.com"

'''
Note: The test below test can return false positives -- e.g. the DNS lookup may return 
a server within the local network. To be really sure you are connected to the internet, 
and talking to a valid host, be sure to use more sophisticated methods (e.g. SSL).
'''
def isConnected():
	try:
    	# see if we can resolve the host name and tells us if there is a DNS listening
		host = socket.gethostbyname(REMOTE_SERVER)
    	# connect to the host -- tells us if the host is actually reachable
		s = socket.create_connection((host, 80), 2)
		return True
	
	except:
		pass
	
	return False

def sphinxRecog(audio):
	# recognize speech using Sphinx
	enterTime = time.time()
	outText = -1

	try:
		outText = r.recognize_sphinx(audio)
		# print colored("\nI think you said --- " + outText + "\n",'green')
	
	except sr.UnknownValueError:
		ip.play("I didn't get it, come again?")
		print colored("\nDidn't get it, try again!\n",'red')
	
	except sr.RequestError as e:
		# print("Sphinx error; {0}".format(e))
		ip.play("Please try again")
		print colored("\nDidn't get it, try again!\n",'red')
	
	# print colored("\nSphinx Time : "+str((time.time())-enterTime)+"\n",'yellow')

	return outText

r = sr.Recognizer()

def googleRecog(audio):
	# useful for hindi recognition
	# recognize speech using Google Voice Recognition
	outText = -1
	b = time.time()

	try:
		outText = r.recognize_google(audio)
		# print colored("\nI think you said --- " + outText + "\n",'green')
	except:
		pass

	# print colored("\nGoogle Time : "+str(time.time()-b)+"\n",'yellow')

	return outText	# return string on success otherwise -1

def bingRecog(audio):
	# recognize speech using Microsoft Bing Voice Recognition
	enterTime = time.time()
	outText = -1
	outNumber = -1

	try:
		json = r.recognize_bing(audio, key="3442db648c654dcabd226893d5503a9d", show_all=True)
		# check if success is returned or not
		checkSuccess = (json[u'header'])[u'status']
		
		if(checkSuccess=='success'):
			confidence = ((json[u'results'])[0])[u'confidence']
			# case when confidence is low
			if(confidence<0.75):
				# error message
				ip.play("I didn't get it, come again?")
				print colored("\nDidn't get it, try again!\n",'red')
			# crosses only if confidence is high
			# print("Confidence = "+confidence)
			outText = ((json[u'results'])[0])[u'lexical']
			# outNumber will contain a number in case if one is spoken(eg., one two three)
			outNumber = ((json[u'results'])[0])[u'name']
			# print colored("\nI think you said --- "+outText+"\n",'green')
			# print colored("\nNumber : "+outNumber+"\n",'green')

	except:
		pass
	
	# print colored("\nBing Time : "+str((time.time())-enterTime)+"\n",'yellow')
	
	return (outText,outNumber)	# return string on success otherwise -1