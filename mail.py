# Functions : mailDriver, mail

from termcolor import colored
import indepFunc as ip
import conRecog as cr
import smtplib
import os

def mailDriver(device):
	while(True):
		print colored("\nTell me receiver's name..\n",'yellow')
		ip.play("Tell me receiver's name..")
		
		audio = ip.recordAudio(device)
		if(cr.isConnected()):	outText = cr.bingRecog(audio)[0]
		else:	outText = cr.sphinxRecog(audio)

		if(outText==-1):
			# if text is not recognized, continue listening
			continue
		elif(outText in ["exit","Exit","exact","Exact"]):
			# exit the whole script
			print colored("\nEnding Session..\n",'red')
			ip.play("Ending Session")
			return
		else:
			print colored("\nShould I serch for "+outText+". Yes or No?\n",'green')
			ip.play("Should I search for "+outText+". Yes or No?")

        	consent = -1
        	while(consent==-1):
        		audio = ip.recordAudio(device)
        		if(cr.isConnected()):	consent = cr.bingRecog(audio)[0]
        		else:	consent = cr.sphinxRecog(audio)

        		if(consent==-1):
        			print colored("Didn't get it, recording again!",'red')
        			ip.play("Didn't get it, recording again!")

			if(consent.lower() in ["yes","yah","ya","yup","yes please"]):
				name = outText.lower()
				if(device==1):	os.chdir('/home/piyush/final')
				else:	os.chdir('/home/pi/final')
				
				# open contacts list
				f = open("contacts.txt","r")
				nameFound = False
				while(True):
					line = (f.readline()).strip()
					if not line: break
					# match every name with recorded name
					if(line.startswith(name)):
						# contacts is a txt file with csvs : name,email
						contactList = line.split(",")
						print colored("\nShould I send it to "+contactList[0]+"?\n",'yellow')
						ip.play("Should I send it to "+contactList[0]+"?")
                        
						# record consent for name
						consent = -1
						while(consent==-1):
							audio = ip.recordAudio(device)
							if(cr.isConnected()):	consent = cr.bingRecog(audio)[0]
							else:	consent = cr.sphinxRecog(audio)

							if(consent==-1):
								print colored("Didn't get it, recording again!",'red')
								ip.play("Didn't get it, recording again!")

                        # if name is matched
						if(consent.lower() in ["yes","yah","ya","yup","yes please"]):
							nameFound = True
							# extract email
							email = line.split(",")[1]
							break

						else: continue

				if(nameFound==True):
					mail(email,device)
					return
				else:
					print colored("\nNo one with such name found!\n",'red')
					ip.play("No one with such name found!")
					continue
			else:
				continue

def mail(receiver_email,device):
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

	# ping the smtp server
	smtpObj.ehlo()

	# start a ssl connection
	smtpObj.starttls()

	# sender email and password
	sender_email = 'piyush15071@gmail.com'
	account_password = 'Dark717)held'
    
    # try to login, a frequent error occurs here
	try:	smtpObj.login(sender_email, account_password)
	except:
		print colored("\nLogin Error!\n",'red')
		ip.play("Login error!")
		return

	while(True):
		print colored("\nRecording subject of the mail..\n",'yellow')
		ip.play("Recording subject of the mail..")
		
		audio = ip.recordAudio(device)
		if(cr.isConnected()):	outText = cr.bingRecog(audio)[0]
		else:	outText = cr.sphinxRecog(audio)

		if(outText==-1):
			# if text is not recognized, continue listening
			continue
		elif(outText in ["exit","Exit","exact","Exact"]):
			# exit the whole script
			print colored("\nEnding Session..\n",'red')
			ip.play("Ending Session")
			smtpObj.quit()
			return
		else:
			print colored("\nSubject is, "+outText+". Is this correct?\n",'green')
			ip.play("Subject is, "+outText+". Is this correct?")

			audio = ip.recordAudio(device)
			if(cr.isConnected()):	consent = cr.bingRecog(audio)[0]
			else:	consent = cr.sphinxRecog(audio)

			if(consent.lower() in ["yes","yah","ya","yup","yes please"]):
				SUBJECT = outText
				break
			else:
				continue

	while(True):
		print colored("\nRecording body of the mail..\n",'yellow')
		ip.play("Recording body of the mail..")
		
		audio = ip.recordAudio(device)
		if(cr.isConnected()):	outText = cr.bingRecog(audio)[0]
		else:	outText = cr.sphinxRecog(audio)

		if(outText==-1):
			# if text is not recognized, continue listening
			continue
		elif(outText in ["exit","Exit","exact","Exact"]):
			# exit the whole script
			print colored("\nEnding Session..\n",'red')
			ip.play("Ending Session")
			smtpObj.quit()
			return
		else:
			print colored("\nBody is, "+outText+". Is this correct?\n",'green')
			ip.play("Body is, "+outText+". Is this correct?")

			audio = ip.recordAudio(device)
			if(cr.isConnected()):	consent = cr.bingRecog(audio)[0]
			else:	consent = cr.sphinxRecog(audio)

			if(consent.lower() in ["yes","yah","ya","yup","yes please"]):
				TEXT = outText
				break
			else:
				continue

	# create message object
	message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

	try:
		# send mail
		smtpObj.sendmail(sender_email, receiver_email, message)
		print colored("\nSuccessfully sent email\n",'green')
	except:
		print colored("\nEmail not sent\n",'red')

	# object needs to be closed
	smtpObj.quit()
	return