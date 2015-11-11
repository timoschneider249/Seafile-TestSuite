#!/usr/bin/python
import subprocess
import os
from urllib2 import Request, urlopen, HTTPError, URLError
import re
import urllib
import urlparse
import mechanize
import cookielib
import sys
import getopt
import difflib
import urllib2
from BeautifulSoup import BeautifulSoup as BS
import re
import requests
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
import time
from bs4 import BeautifulSoup as BS4
import getpass

#####https://github.com/haiwen/seafile/blob/master/python/seaserv/api.py#####
class Token:
	pass
username = "seafile-ta-01@uni-mainz.de"
password = "Wurzel16ist4"
s = ""	
output_filename = "visited.txt"
visited = []
urls = []
allLinks = []
brokenLinks = []
images = []
brokenImages = []
websiteImages =[]
newurl = ""
pdfs = []
brokenPDF = []
iteration = 0
pattern = "seafile.rlp.net"
MaxIteration = 9999


     	
def checkLink(url,visi,br,iteration,fileOutput,types,pattern, MaxIteration):
	# Set the startingpoint for the spider and initialize 
	# the a mechanize browser object
	# Since the amount of urls in the list is dynamic
	#   we just let the spider go until some last url didn't
	#   have new ones on the webpage
	# Selenium Stuff

	
	#

	img_counter = 0
	if fileOutput == False:
		print "*"*50
		print "Checkin site "+urls[0]

	br.open(urls[0])
	currentUrl = urls.pop(0)
	#print currentUrl
	
	r = requests.head(url)
	if "text/html" in r.headers["content-type"]:
		soup = BS(br.response().read())

		for img in soup.findAll('img'):
			
			img = img['src']
			
			for imgTypes in types:
				if imgTypes in img:

					try:
						if "http" not in img:
							parsedLink = urlparse.urlsplit(currentUrl)							
							img = parsedLink.scheme+"://"+parsedLink.netloc+"/"+img

						r = requests.head(img)
						if r.status_code == requests.codes.ok:
							if fileOutput == False:
								print "found image: %s" %(img)
								print "image is available"
							images.append(img)
							img_counter +=1
								
						else:
							if fileOutput == False:
								print "found image: %s" %(img)
								print "image site is down"
							brokenImages.append(img)
							img_counter +=1
					except requests.HTTPError, e:
						print "HTTP ERROR %s occured" % e.code
					except (requests.exceptions.MissingSchema) as e:
						print "Missing schema occured. status %s"%e
						print e		
					
			
			if types is "":
					try:
						#google only
						if img.startswith("//"):
							img = img[2:]
							img = "http://"+img
							print img
						elif "http" not in img or "www." not in img:
							#print img
							parsedLink = urlparse.urlsplit(currentUrl)
							#print parsedLink							
							img = parsedLink.scheme+"://"+parsedLink.netloc+"/"+img
							#print img


						r = requests.head(img)
						if r.status_code == requests.codes.ok:
							if fileOutput == False:
								print "found image: %s" %(img)
								print "image is available"

								
							images.append(img)
							img_counter +=1								
						else:
							if fileOutput == False:
								print "found image: %s" %(img)
								print "image site is down"
							brokenImages.append(img)
							img_counter +=1
					except requests.HTTPError, e:
						print "HTTP ERROR %s occured" % e.code
					except (requests.exceptions.MissingSchema) as e:
						print "Missing schema occured. status %s"%e
						print e	
					
			
		if fileOutput == False:
			print "*"*50
			print "Number of images on this site %d"%(img_counter)
			print "Number of images: %d"%(len(images))

		for link in br.links():
			if iteration < MaxIteration:

				try:	
					
					newurl =  urlparse.urljoin(link.base_url,link.url)
					allLinks.append(newurl)
					if pattern != "seafile.rlp.net":

						check= re.search(pattern, newurl, flags=re.IGNORECASE)
						if newurl not in visited and check is not None:
							print "Found regex: '%s' in URL: %s" %(check.group(0),newurl)
							visited.append(newurl)
							urls.append(newurl)
							
							if fileOutput == False:
								print "found: " +newurl
								print "Iteration: %d" %(iteration)
							checkLink(newurl,newurl,br,iteration+1,fileOutput,types,pattern,MaxIteration)
					else:
						if newurl not in visited and pattern in newurl:
							visited.append(newurl)
							urls.append(newurl)
							
							if fileOutput == False:
								print "found: " +newurl
								print "Iteration: %d" %(iteration)
							checkLink(newurl,newurl,br,iteration+1,fileOutput,types,pattern,MaxIteration)


				except (mechanize.HTTPError,mechanize.URLError) as e:
					brokenLinks.append("Found: %s on site %s with Error Code %s"%(newurl,currentUrl,e))
					if fileOutput == False:
						print 'HTTP ERROR %s occured' % e
					urls.pop(0)
			else:
				if fileOutput == False:
					print >>sys.stderr, "Reached max iteration"

	else:
		try:

			if "pdf" in currentUrl:
				print "Pdf file found"
				r = requests.head(currentUrl)
				if r.status_code == requests.codes.ok:
					if fileOutput == False:
						print "found pdf: %s" %(currentUrl)
						print "pdf is available"
					pdfs.append(currentUrl)
				else:
					if fileOutput == False:
						print "PDF site is down"
					brokenPDF.append(currentUrl)
			elif ".jpg" in currentUrl:
				r = requests.head(currentUrl)
				if r.status_code == requests.codes.ok:
					if fileOutput == False:
						print "found image: %s" %(currentUrl)
						print "image is available"
					images.append(currentUrl)
				else:
					if fileOutput == False:
						print "PDF site is down"
					brokenImages.append(currentUrl)
			else:
				print "Non html found"

		except requests.HTTPError, e:
			print "HTTP ERROR %s occured" % e.code
		except (requests.exceptions.MissingSchema) as e:
			print "Missing schema occured. status %s"%e
			print e	
		except: 
			print "Unkown error"

def checkLinkSelenium(url,visi,browser,iteration,fileOutput,types,pattern, MaxIteration):
	# Set the startingpoint for the spider and initialize 
	# the a mechanize browser object
	# Since the amount of urls in the list is dynamic
	#   we just let the spider go until some last url didn't
	#   have new ones on the webpage


	img_counter = 0
	if fileOutput == False:
		print "*"*50
		print "Checkin site "+urls[0]

	browser.get(urls[0])
	currentUrl = urls.pop(0)

	
	r = requests.head(url)
	if "text/html" in r.headers["content-type"]:
		browser.get(currentUrl)  

		element_to_hover_over = browser.find_element_by_class_name("op-container")
		hover = AC(browser).move_to_element(element_to_hover_over)
		hover.perform()

		html_source = browser.page_source  	

		soup = BS4(html_source,'html.parser')  

		for img in soup.findAll('img'):

			img = img['src']
			
			if types is "":
				try:
					#google only
					if img.startswith("//"):
						img = img[2:]
						img = "http://"+img
						print img
					elif "http" not in img or "www." not in img:
						#print img
						parsedLink = urlparse.urlsplit(currentUrl)
						#print parsedLink							
						img = parsedLink.scheme+"://"+parsedLink.netloc+"/"+img
						#print img

					r = requests.head(img)
					if r.status_code == requests.codes.ok:
						if fileOutput == False:
							print "found image: %s" %(img)
							print "image is available"
								
						images.append(img)
						img_counter +=1								
					else:
						if fileOutput == False:
							print "found image: %s" %(img)
							print "image site is down"
						brokenImages.append(img)
						img_counter +=1
				except requests.HTTPError, e:
					print "HTTP ERROR %s occured" % e.code
				except (requests.exceptions.MissingSchema) as e:
					print "Missing schema occured. status %s"%e
					print e	
				
			
		if fileOutput == False:
			print "*"*50
			print "Number of images on this site %d"%(img_counter)
			print "Number of images: %d"%(len(images))
		browser.quit()
		sys.exit(0)
		for link in br.links():
			if iteration < MaxIteration:

				try:	
					
					newurl =  urlparse.urljoin(link.base_url,link.url)
					allLinks.append(newurl)
					if pattern != "seafile.rlp.net":

						check= re.search(pattern, newurl, flags=re.IGNORECASE)
						if newurl not in visited and check is not None:
							print "Found regex: '%s' in URL: %s" %(check.group(0),newurl)
							visited.append(newurl)
							urls.append(newurl)
							
							if fileOutput == False:
								print "found: " +newurl
								print "Iteration: %d" %(iteration)
							checkLink(newurl,newurl,br,iteration+1,fileOutput,types,pattern,MaxIteration)
					else:
						if newurl not in visited and pattern in newurl:
							visited.append(newurl)
							urls.append(newurl)
							
							if fileOutput == False:
								print "found: " +newurl
								print "Iteration: %d" %(iteration)
							checkLink(newurl,newurl,br,iteration+1,fileOutput,types,pattern,MaxIteration)


				except (mechanize.HTTPError,mechanize.URLError) as e:
					brokenLinks.append("Found: %s on site %s with Error Code %s"%(newurl,currentUrl,e))
					if fileOutput == False:
						print 'HTTP ERROR %s occured' % e
					urls.pop(0)
			else:
				if fileOutput == False:
					print >>sys.stderr, "Reached max iteration"

	else:
		try:

			if "pdf" in currentUrl:
				print "Pdf file found"
				r = requests.head(currentUrl)
				if r.status_code == requests.codes.ok:
					if fileOutput == False:
						print "found pdf: %s" %(currentUrl)
						print "pdf is available"
					pdfs.append(currentUrl)
				else:
					if fileOutput == False:
						print "PDF site is down"
					brokenPDF.append(currentUrl)
			elif ".jpg" in currentUrl:
				r = requests.head(currentUrl)
				if r.status_code == requests.codes.ok:
					if fileOutput == False:
						print "found image: %s" %(currentUrl)
						print "image is available"
					images.append(currentUrl)
				else:
					if fileOutput == False:
						print "PDF site is down"
					brokenImages.append(currentUrl)
			else:
				print "Non html found"

		except requests.HTTPError, e:
			print "HTTP ERROR %s occured" % e.code
		except (requests.exceptions.MissingSchema) as e:
			print "Missing schema occured. status %s"%e
			print e	
		except: 
			print "Unkown error"

def output(visited, allLinks, brokenLinks, fileOutput,output_filename, images):
	i = 0

	if fileOutput == False:
		print "*"*50
		print "visited"	
		for item in visited:
			print item
		print "*"*50
		print "all Links"	
		#for item in allLinks:
			#print item
		print "*"*50
		print "broken Links"	
		for item in brokenLinks:
			print item
		print "*"*50
		print "images"	
		for item in images:
			print item
		print "*"*50
		print "Total number of links found: %d"%len(allLinks)
		print "Total number of distinct links found: %d"%len(visited)
		print "Total number of dead links found: %d"%len(brokenLinks)
		print "Total number images found: %d"%len(images)
	else:
		print "*"*50
		print "Output filename was set to "+output_filename
		writeFile = open(output_filename,"w")
		writeFile.write("<<<<visited>>>>\n\n")	
		for item in visited:
			i +=1
			writeFile.write("%d. %s \n"%(i,item))
		i = 0
		writeFile.write("<<<<brokenLinks>>>>\n\n")	
		for item in brokenLinks:
			i +=1
			writeFile.write("%d. %s \n"%(i,item))
		i = 0
		writeFile.write("<<<<<allLinks>>>>>\n\n")
		for item in allLinks:
			i +=1
			writeFile.write("%d. %s \n"%(i,item))
		i = 0
		writeFile.write("<<<<visited>>>>\n\n")
		for item in images:
			i +=1
			writeFile.write("%d. %s \n"%(i,item))
		writeFile.close()



def login(fileOutput,output_filename,types,pattern,site,MaxIteration):

	if site is "":
		url = "https://seafile.rlp.net/"
		visited.append(url)
		urls.append(url)
		# Browser 
		br = mechanize.Browser() 
		

		

		if output_filename and fileOutput==True:
			print "Running program with outputfile "+output_filename
		if fileOutput==False and output_filename is None:
			print "Starting program without file output"

			
		if fileOutput==True and output_filename is None:
			output_filename="output.txt"
		
		# Enable cookie support for urllib2 
		cookiejar = cookielib.LWPCookieJar() 
		br.set_cookiejar( cookiejar ) 

		# Browser options 
		br.set_handle_equiv( True ) 
		br.set_handle_redirect( True ) 
		br.set_handle_referer( True ) 
		br.set_handle_robots( False ) 

		# ?? 
		#br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 

		br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 

		# authenticate 
		br.open("https://seafile.rlp.net/accounts/login/?next=/") 
		br.select_form( nr = 2 ) 
		# these two come from the code you posted
		# where you would normally put in your username and password
		br[ "username" ] = username
		br[ "password" ] = password
		res = br.submit() 
		url = br.open("https://seafile.rlp.net/profile/" ) 
		returnPage = url.read() 
		#print returnPage
		print "Successfully logged in as "+username+"!\n"
		if fileOutput == True:
			print "writing files..."
		if MaxIteration != 9999:
			print "MaxIteration set to: %d"%MaxIteration
		checkLink(urls[0],visited[0],br,iteration,fileOutput,types,pattern,MaxIteration)
		output(visited,allLinks,brokenLinks, fileOutput,output_filename, images)
	else:
		print "Starting to crawl on site: %s" %site
		br = mechanize.Browser() 
		if output_filename and fileOutput==True:
			print "Running program with outputfile "+output_filename
		if fileOutput==False and output_filename is None:
			print "Starting program without file output"

			
		if fileOutput==True and output_filename is None:
			output_filename="output.txt"
		
		# Enable cookie support for urllib2 
		cookiejar = cookielib.LWPCookieJar() 
		br.set_cookiejar( cookiejar ) 

		# Browser options 
		br.set_handle_equiv( True ) 
		br.set_handle_redirect( True ) 
		br.set_handle_referer( True ) 
		br.set_handle_robots( False ) 

		# ?? 
		#br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 

		br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 
		visited.append(site)
		urls.append(site)
		br.open(site) 
		checkLink(urls[0],visited[0],br,iteration,fileOutput,types,pattern, MaxIteration)
		output(visited,allLinks,brokenLinks, fileOutput,output_filename, images)
	

def loginSelenium(fileOutput,output_filename,types,pattern,site,MaxIteration):
	username =raw_input("Username: ")
	password = getpass.getpass("Password: ")
	if site is "":
		url = "https://seafile.rlp.net/"
		browser = webdriver.Firefox()
		browser.implicitly_wait(10)
		browser.get(url)
		
		print "open hidden login :3"
		local_input = browser.find_element_by_id("toggle_local_login").click()
		
		print "Searching usernameId"
		usernameId = browser.find_element_by_name("username")
		print "Searching passwordId"
		
		passwordId = browser.find_element_by_name("password")
		usernameId.send_keys(username) 
		passwordId.send_keys(password)
		print "login attempt"
		login_attempt = browser.find_element_by_xpath("//*[@type='submit']")
		login_attempt.submit()

		visited.append(url)
		urls.append(url)

		if output_filename and fileOutput==True:
			print "Running program with outputfile "+output_filename
		if fileOutput==False and output_filename is None:
			print "Starting program without file output"

			
		if fileOutput==True and output_filename is None:
			output_filename="output.txt"

		if fileOutput == True:
			print "writing files..."
		if MaxIteration != 9999:
			print "MaxIteration set to: %d"%MaxIteration
		time.sleep(3)
		html_source = browser.page_source  	
		soup = BS4(html_source,'html.parser')  

		login_check = soup.findAll('img',{'class':'avatar'}) 
		
		if not login_check:
			print "username or password incorrect"
			browser.quit()
			sys.exit(0) 
		else:
			print "Successfully logged in as %s" %username

		checkLinkSelenium(urls[0],visited[0],browser,iteration,fileOutput,types,pattern,MaxIteration)
		output(visited,allLinks,brokenLinks, fileOutput,output_filename, images)

def compareLinks(fileInput1,fileInput2):

	with open(fileInput1, 'r') as hosts0:
		with open(fileInput2, 'r') as hosts1:
			diff = difflib.ndiff(hosts0.readlines(),hosts1.readlines())
			for line in diff:
				if line.startswith("-"):
					print "Row is missing in file 2"
					print line
				if line.startswith("+"):
					print "Row is missing in file 1"
					print line
	print "Done"





if len(sys.argv) == 1:
	print "Running programm without parameters"
	fileOutput = False
	output_filename = None
	types = ""
	site = ""
	pattern = "seafile.rlp.net"
	login(fileOutput,output_filename,types,pattern,site,MaxIteration)

	

parser = argparse.ArgumentParser(description='This is a TestSuite script by Timo Schneider.')
parser.add_argument('-o', '--output',					help='-o 	: creates output file, requires name of file')
parser.add_argument('-q', '--quiet',		action='store_true',	help='-q 	: Program runs without output and no prints')
parser.add_argument('-p', '--ping',		action='store_true',	help='-p 	: Ping the api of seafile.uni-mainz.de')
parser.add_argument('-c', '--compare', 		nargs='+',		help='-c 	: Compares two files, if there is no output the files are equal')
parser.add_argument('-t', '--token',		action='store_true' ,	help='-t 	: Reiceive a token and ping it')
parser.add_argument('-ty', '--types',		nargs = '*' ,		help='-ty 	: For image searching, receives an image extention for example .png or .gif')
parser.add_argument('-d', '--debug',					help='-d 	: Testing all the methods if they work correctly *not implemented yet*')
parser.add_argument('-v', '--verbose',					help='-v 	: quiet run *Not implemented yet*')
parser.add_argument('-pa', '--pattern',					help='-pa 	: Change the pattern, default is seafile.rlp.net, None means no pattern!')
parser.add_argument('-s', '--start',					help='-s 	: Change start site of crawling, default is https://seafile.rlp.net/accounts/login/?next=/')
parser.add_argument('-i', '--iteration',		type=int,		help='-i 	 	: Change max Number of Iterations, default is infinite')
parser.add_argument('-pas', '--patternStart',	nargs='+',		help='-pas 	: Define a starting page, afterwords choose a search pattern')
parser.add_argument('-is', '--iterationStart',	nargs='+',		help='-is  	: Change max Number of Iterations, default is infinite. Also lets you define a starting page, example: 5 http://www.google.com')
parser.add_argument('-isp', '--iterationStartPattern',	nargs='+',	help='-isp  	: First give max iteration and starting page, afterwords define pattern')
parser.add_argument('-ls', '--liveSearch',		action='store_true',	help='-ls	: Using selenium to search even javascript based links and images')

args = parser.parse_args()

if args.output:
	output_filename = args.output
	fileOutput = True
	types = ""
	pattern = "seafile.rlp.net"
	site = "" 
	login(fileOutput,output_filename,types,pattern,site,MaxIteration)

if args.quiet:
	output_filename = None
	fileOutput = False
	pattern = "seafile.rlp.net"
	types = ""
	site = ""
	login(fileOutput,output_filename,types,pattern,site,MaxIteration)



if args.compare:
	print "Comparing two files"
	file1 = args.compare[0]
	file2 = args.compare[1]
	compareLinks(file1,file2)


if args.types:
	print "types to search %s"%args.types
	output_filename = None
	pattern = "seafile.rlp.net"
	fileOutput = False
	site = ""
	login(fileOutput,output_filename,args.types,pattern,site,MaxIteration)

if args.pattern:
	print "You changed the pattern to: " +args.pattern
	pattern = args.pattern
	output_filename = None
	fileOutput = False
	types = ""
	site = ""
	login(fileOutput,output_filename,types,pattern,site,MaxIteration)

if args.start:
	output_filename = None
	fileOutput = False
	types = ""
	site = args.start
	pattern = ""
	login(fileOutput,output_filename,types,pattern,site,MaxIteration)

if args.iteration:
	output_filename = None
	fileOutput = False
	types = ""
	site = ""
	pattern = "seafile.rlp.net"
	MaxIteration = args.iteration
	login(fileOutput,output_filename,types,pattern,site,MaxIteration)

if args.patternStart:
	print "You changed the pattern to: " +str(args.patternStart[0])
	pattern = str(args.patternStart[0])
	output_filename = None
	fileOutput = False
	types = ""
	site = str(args.patternStart[1])
	login(fileOutput,output_filename,types,pattern,site,MaxIteration)

if args.iterationStart:
	output_filename = None
	fileOutput = False
	types = ""
	MaxIteration = int(args.iterationStart[0])
	site = str(args.iterationStart[1])
	pattern = ""
	login(fileOutput,output_filename,types,pattern,site,MaxIteration)

if args.iterationStartPattern:
	print "You changed the pattern to: %s" %(str(args.iterationStartPattern[2]))
	output_filename=None
	fileOutput = False
	types = ""
	MaxIteration = int(args.iterationStartPattern[0])
	site = str(args.iterationStartPattern[1])
	pattern =  str(args.iterationStartPattern[2])
	login(fileOutput,output_filename,types,pattern,site,MaxIteration)

if args.liveSearch:
	print "Running programm with Selenium"
	fileOutput = False
	output_filename = None
	types = ""
	site = ""
	pattern = "seafile.rlp.net"
	MaxIteration = 9999
	loginSelenium(fileOutput,output_filename,types,pattern,site,MaxIteration)
