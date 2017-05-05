# Functions : search, searchNews


# e.g, donald trump, who is donald trump, president of india
# side-vala
# ("div", { "class" : "_tXc" })

# e.g, what is internet / word meanings
# ("table", { "style" : "font-size:14px;width:100%" })

# e.g, shape of you
# ("div", { "class" : "_o0d" })
# find the video url and play it using youtube.py

# e.g, how to wash dishes
# ("div", { "class" : "_o0d" })

import urllib
import urllib2
import os
from bs4 import BeautifulSoup
from termcolor import colored
import youtube as you
import time
import indepFunc as ip

# headers for a mozilla browser
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

def search(inp,device):
	# below lines generate a google search url from search text
	pieces = inp.split(" ")

	query = ""

	for k in range(len(pieces)):
		pieces[k] = pieces[k].lower()
		if(k!=len(pieces)-1):
			query += pieces[k]+"+"
		else:
			query += pieces[k]

	url = "https://www.google.co.in/search?site=&source=hp&q="
	url += query
	# print colored("\n"+url+"\n",'yellow')

	# web scraping google is forbidden, hence headers are needed as a workaround
	headers={'User-Agent':user_agent,} 

	request=urllib2.Request(url,None,headers)
	response = urllib2.urlopen(request)
	
	# complete code is saved in "code"
	code = response.read()

	# save code file offline as "page_content.html"
	with open('page_content.html', 'wb') as fid:
	    fid.write(code)

	# make a soup object from html code
	soup = BeautifulSoup(code,"html.parser")

	# found will be None if the specified tags are not found in code
	
	found = soup.find("div", { "class" : "_tXc" })
	if(found==None):
		found = soup.find("table", { "style" : "font-size:14px;width:100%" })
		if(found!=None):
			# delete the prefix noun/pronoun/verb/adjective
			toDelete = soup.find("div", { "style" : "color:#666;padding:5px 0" }).get_text()
			output = found.get_text()
			output = output[len(toDelete):]
			print colored("\n"+output+"\n",'yellow')
			ip.play(output)
		else:
			found = soup.find("div", { "class" : "_o0d" })
			if(found!=None):
				output = found.get_text()
				
				# if the top result is a youtube video, play it using youtube function
				if(output.find("https://www.youtube.com/watch?v=")!=-1):
					link = output[output.find("https"):]
					ip.play("Playing youtube video..")
					print colored("\nPlaying youtube video..\n",'green')
					you.youtube(link,1,device)
				else:
					print colored("\n"+output+"\n",'yellow')
					ip.play(output)
			else:
				# no straightaway answer from google, only webpages available
				print colored("\nWill mail the link to you.\n",'green')
				ip.play("Will mail the link to you.")
	else:
		output = found.get_text()
		print colored("\n"+output+"\n",'yellow')
		ip.play(output)

	# remove the html code once function finishes
	os.system("rm page_content.html")

def searchNews():
	url = "https://www.google.co.in/search?q=news&source=lnms&tbm=nws&sa=X"
	# print colored("\n"+url+"\n",'yellow')

	# web scraping google is forbidden, hence headers are needed as a workaround
	headers={'User-Agent':user_agent,} 

	request=urllib2.Request(url,None,headers)
	response = urllib2.urlopen(request)
	
	# complete code is saved in "code"
	code = response.read()

	# save code file offline as "page_content.html"
	with open('page_content.html', 'wb') as fid:
	    fid.write(code)

	# make a soup object from html code
	soup = BeautifulSoup(code,"html.parser")

	found = soup.findAll("h3", { "class" : "r" })
	if(found==None):
		print colored("\nSomething went wrong, please try again.\n",'red')
		ip.play("Something went wrong, please try again.")
	else:
		# loop through all headlines, get_text and play text
		for t in found:
			text = t.get_text()
			print colored("\n"+text+"\n",'green')
			ip.play(text)