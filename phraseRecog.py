# Functions : phraseRecog

from termcolor import colored
from time import sleep
import indepFunc as ip
import phraseRecog as pr
import conRecog as cr
import playOffline as po
import youtube as you
import speech_recognition as sr
import mail
import alarm
import google
import calender
import os

r = sr.Recognizer()

# actions that can be performed
phraseList = ["movie","Movie","movies","Movies","music","Music","schedule","Schedule"
			  "Search","search","mail","Mail","alarm","Alarm","youtube","Youtube",
			  "YouTube","Photos","photos","photo","Photo","News","news","new","New",
			  "man","Man""Men","men","male","Male"]

# list to be displayed everytime asking for phrase words
phrases = ["Movie","Music","Schedule","Search","Mail","Alarm","Youtube","Photos","News"]

# "Victoria" is often recognized as words in list below
triggerList = ["victoria","victorious","pictorial","victoriya","call victoria","pretoria","vicktoria"]

# controls available while playing the video
videoControls = ["play","stop","pause","volume up","volume down"]

# keypress sequences to simulate video controls
stop_sequence = '''keydown Q
keyup Q
'''

pause_sequence = '''keydown P
keyup P
'''

volume_down_sequence = '''keydown 9
keyup 9
'''

volume_up_sequence = '''keydown 0
keyup 0
'''

# main driver function of whole project
def phraseRecog(device):
	print colored("\nTell me the phrase word!\n",'green')
	ip.play("Tell me the phrase word!")

	while(True):
		print colored("\nPhraseList : ",'yellow')
		print colored(phrases,'yellow')
		print("\n")
		
		sleep(2)

		# listen to the phrase word
		audio = ip.recordAudio(device)
                if(cr.isConnected()):
                        if(device==1):	outText = cr.googleRecog(audio)
                        else:	outText = cr.bingRecog(audio)[0]
		else: outText = cr.sphinxRecog(audio)

		# if voice not recognized
		if(outText==-1):
			print colored("\nDidn't get it, please try again\n",'red')
			ip.play("Didn't get it, please try again")

		# if user says exit, return from the main function
		elif(outText in ["exit","Exit"]):
			print colored("\nEnding Session..\n",'red')
			ip.play("Ending Session")
			return
		
		# if voice is recognized and it is not "exit"
		else:
			# convert to lower letters for easier comparison
			outText = outText.lower()

			# if word is a phrase word
			if(outText in phraseList):
				# if movie is said
				if(outText in ["movie","movies"]):
					print colored("\nWhich movie to play?\n",'green')
					ip.play("Which movie to play?")
					while(True):
						# print all movie names by printing out.txt
						print colored("Possible Options :",'green')
						if(device==1):	os.chdir('/home/piyush/ied/movies')
						else:	os.chdir('/home/pi/ied/movies')	
						os.system('cat out.txt')
						print ("\n")

						# record movie name
						audio = ip.recordAudio(device)
						if(cr.isConnected()): movieName = cr.bingRecog(audio)[0]
						else: movieName = cr.sphinxRecog(audio)

						# if user says exit, exit main function
						if(movieName in ["exit","Exit","exact","Exact"]):
								print colored("\nEnding Session..\n",'red')
								ip.play("Ending Session")
								return

						# po.playMovie(movieName) returns false if movie doesn't exist
						# plays the movie and returns true if movie exists
						if(po.playMovie(movieName,device)): return
						
						else:
							# if po.playMovie(movieName) returns false, give error message
							print colored("\nNo movie with such name exists! Try again.\n",'red')
							ip.play("No movie with such name exists! Try again.")

				# if music is said
				elif(outText in ["music"]):
					# ask if user wants to play specific track or shuffle all the avail. tracks
					print colored("\nTrack or shuffle\n",'green')
					ip.play("Track or shuffle")

					while(True):
						# record tracks or shuffle
						audio = ip.recordAudio(device)
						if(cr.isConnected()): musicOption = cr.bingRecog(audio)[0]
						else: musicOption = cr.sphinxRecog(audio)
						
						# if user says exit, return the main function
						if(musicOption in ["exit","Exit","exact","Exact"]):
								print colored("\nEnding Session..\n",'red')
								ip.play("Ending Session")
								return

						# if track is said
						if(musicOption in ["track","Track"]):
							print colored("Which track to play?",'green')
							ip.play("Which track to play?")

							while(True):
								# print all the possible options by printing out.txt
								print colored("\nPossible Options :\n",'green')
								if(device==1):	os.chdir('/home/piyush/ied/music')
								else:	os.chdir('/home/pi/ied/music')
								os.system('cat out.txt')
								print("\n")

								# record track name
								audio = ip.recordAudio(device)
								if(cr.isConnected()): musicName = cr.bingRecog(audio)[0]
								else: musicName = cr.sphinxRecog(audio)
								
								# if exit is said, exit the main function
								if(musicName in ["exit","Exit","exact","Exact"]):
									print colored("\nEnding Session..\n",'red')
									ip.play("Ending Session")
									return

								# po.playTrack(musicName) returns false if track doesn't exist
								# plays the track and returns true if track exists
								if(po.playTrack(musicName,device)): return
								
								else:
									# if po.playMovie(movieName) returns false, give error message
									print colored("\nNo track with such name exists! Try again.\n",'red')
									ip.play("No track with such name exists! Try again.")
						
						# if user wants to shuffle tracks
						elif(musicOption in ["shuffle","Shuffle"]):
							po.shuffle(device)
							return
						
						# if user says something instead of track or shuffle
						else:
							print colored("\nWrong Option! Try again.\n",'red')
							ip.play("Wrong Option! Try again.")

				# if photos is said
				# works only for albums stored as folders
				elif(outText in ["photos","photo"]):
					print colored("Which album to play?",'green')
					ip.play("Which album to play?")

					while(True):
						# show all albums stored
						print colored("\nPossible Options :",'green')
						if(device==1):	os.chdir('/home/piyush/ied/photos')
						else:	os.chdir('/home/pi/ied/photos')
						os.system('cat out.txt')

						# recored the album name
						audio = ip.recordAudio(device)
						if(cr.isConnected()): albumName = cr.bingRecog(audio)[0]
						else: albumName = cr.sphinxRecog(audio)

						# if user says exit, exit the main function
						if(albumName in ["exit","Exit","exact","Exact"]):
							ip.play("Ending Session")
							print colored("\nEnding Session..\n",'red')
							return

						# po.playPhotos(albumName) returns false if album doesn't exist
						# plays the album and returns true if album exists
						if(po.playPhotos(albumName,device)): return
						
						else:
							# if po.playPhotos(albumName) returns false, give error message
							print colored("\nNo album with such name exists! Try again.\n",'red')
							ip.play("No album with such name exists! Try again.")

				# to access calender
				# currently programmed to only show upcoming 5 events
				# creating a new event functionality is implemented
				# but not used due to the recognition constraints
				# future scope : add insertion and deletion of events
				elif(outText == "schedule"):
					print colored("\nUpcoming events are..\n",'green')
					ip.play("Upcoming events are")
					calender.main()
					return

				# if alarm is said
				# sets an alarm for the first occurrence of the recorded time
				# this won't work offline
				# future scope : tell the date and set an alarm for a particular day
				elif(outText == "alarm"):
					print colored("\nTell me the time?\n",'green')
					ip.play("Tell me the time?")
					while(True):
						# record alarm time
						audio = ip.recordAudio(device)
						if(cr.isConnected()):	(query,time) = cr.bingRecog(audio)
						else:
							print colored("\nNot connected to the internet.\n",'red')
							return

						# if user says exit, exit the main function
						if(query in ["exit","Exit","exact","Exact"]):
							print colored("\nEnding Session..\n",'red')
							ip.play("Ending Session")
							return

						# if text is not understood, record again
						elif(query==-1):
							print("\nWhat did you say?\n",'red')
							ip.play("What did you say?")
							continue

						# if something else is recognized
						else:
							# time -> 8 21 PM
							# query -> eight twenty one PM

							# extract last two words
							ampm = query[len(query)-2:]
							
							# check if they are am or pm
							# if not record again
							if(ampm.lower() not in ["am","pm"]):
								print colored("\nWrong format! Recording again..\n",'red')
								ip.play("Wrong format! Recording again..")
								continue

							# remove last two letters from time and query
							time = time[:len(time)-2]
							query = query[:len(query)-2]
							splitQuery = query.split(" ")
							
							# case because 1 is often recognised as vine
							if(splitQuery[0]=="vine"):
								hour = "1"
								time = time[4:]
							# case because 2 is often recognised as do
							elif(splitQuery[0]=="do"):
								hour = "2"
								time = time[2:]
							elif(splitQuery[0] in ["ten","eleven","twelve"]):
								hour = time[:2]
								time = time[2:]
							else:
								hour = time[:1]
								time = time[1:]
							if(time.startswith(":")):
								time = time[1:]

							minutes = time.strip(" ")
							
							# if minutes is empty
							if(minutes in [None," ",""]):
								minutes = "0"

							try:
								# check if "hour" and "minutes" contains numbers or not
								int(hour)
								int(minutes)
							except:
								print colored("\nWrong format! Recording again..\n",'red')
								ip.play("Wrong format! Recording again..")
								continue

							# confirm the alarm details
							print colored("\nShould I set an alarm for "+hour+" "+minutes+" "+ampm+"? Yes or No?\n",'green')
							ip.play("Should I set an alarm for "+hour+" "+minutes+" "+ampm+"? Yes or No?")
							
							while(True):
								# record consent
								audio = ip.recordAudio(device)
								if(cr.isConnected()): consent = cr.bingRecog(audio)[0]
								else: consent = cr.sphinxRecog(audio)

								consent = str(consent).lower()
								if(consent in ["yes","yah","ya","yup","yes please"]):
									# on confirming set alarm and exit the main function
									alarm.set(hour,minutes,ampm,device)
									return
								
								else:
									# record time again if user says no
									print colored("\nRecording time again..\n",'green')
									ip.play("Recording time again")
									break

				# if user wants to perform a google search
				elif(outText == "search"):
					print colored("\nWhat should I search for?\n",'green')
					ip.play("What should I search for?")
					while(True):
						# record search query
						audio = ip.recordAudio(device)
						if(cr.isConnected()): query = cr.bingRecog(audio)[0]
						else: query = cr.sphinxRecog(audio)
						
						# exit the main function
						if(query in ["exit","Exit","exact","Exact"]):
							print colored("\nEnding Session..\n",'red')
							ip.play("Ending Session")
							return

						# if voice is not understood
						elif(query==-1):
							print colored("\nWhat did you say?\n",'red')
							ip.play("What did you say?")
							continue

						# if voice is recognized
						else:
							# confirm the search query
							print colored("\nShould I search for "+query+"? Yes or No?\n",'green')
							ip.play("Should I search for "+query+"? Yes or No?")
							
							while(True):
								# record consent
								audio = ip.recordAudio(device)
								if(cr.isConnected()): consent = cr.bingRecog(audio)[0]
								else: consent = cr.sphinxRecog(audio)

								try : consent = consent.lower()
								except:
									print colored("\nPardon?\n",'red')
									ip.play("Pardon?")
									continue
									
								if(consent in ["yes","yah","ya","yup","yes please"]):
									# perform the google search and exit the main fucntion
									google.search(query,device)
									return
								
								else:
									# if the user says no to the recognized text
									print colored("\nRecording search query again..\n",'green')
									ip.play("Recording search query again")
									break

				# if user wants news
				elif(outText == "news"):
					google.searchNews()
					return

				elif(outText in ["mail","male","man","men"]):
					mail.mailDriver(device)
					return

				# if user wants to watch a youtube video
				elif(outText == "youtube"):
					print colored("\nWhich video should I search for?\n",'green')
					ip.play("Which video should I search for?")
					while(True):
						# record video name
						audio = ip.recordAudio(device)
						if(cr.isConnected()): videoName = cr.bingRecog(audio)[0]
						else: videoName = cr.sphinxRecog(audio)
						
						# exit the main function
						if(videoName in ["exit","Exit","exact","Exact"]):
							print colored("\nEnding Session..\n",'red')
							ip.play("Ending Session")
							return

						# if text is not understood
						elif(videoName==-1):
							print colored("\nWhat did you say?\n",'red')
							ip.play("What did you say?")
							continue

						# if text is understood
						else:
							# confirm the video name
							print colored("\nShould I search for "+videoName+"? Yes or No?\n",'green')
							ip.play("Should I search for "+videoName+"? Yes or No?")
							
							while(True):
								# record confirmation
								audio = ip.recordAudio(device)
								if(cr.isConnected()): consent = cr.bingRecog(audio)[0]
								else: consent = cr.sphinxRecog(audio)

								consent = consent.lower()
								if(consent in ["yes","yah","ya","yup","yes please"]):
									# play the youtube video and exit main function
									you.youtube(videoName,0,device)
									return
								
								else:
									# if user says no to recognized text, record again
									print colored("\nRecording the video name again..\n",'green')
									ip.play("Recording the video name again")
									break

			# if the word recognied is not a phrase word
			else:
				print colored("\n"+outText+" is not a phrase, try again.\n",'red')
				ip.play(outText+" is not a phrase, try again.")
