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


visited = []
urls = []
allLinks = []
brokenLinks = []
images = []
brokenImages = []
websiteImages =[]
iteration = 0
def checkLink(url,visi,browser,iteration,fileOutput,types,pattern, MaxIteration):
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
	#print currentUrl
	
	r = requests.head(url)
	if "text/html" in r.headers["content-type"]:
		browser.get(currentUrl)  

		element_to_hover_over = browser.find_element_by_class_name("op-container")
		hover = AC(browser).move_to_element(element_to_hover_over)
		hover.perform()

		html_source = browser.page_source  	

		soup = BS4(html_source,'html.parser')  

		for img in soup.findAll('img'):
		
			
			#source1= hidden_object1.get_attribute('src')
			
			#source2= hidden_object2.get_attribute('src')

			#print source1
			#print source2
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

def login(fileOutput,output_filename,types,pattern,site,MaxIteration):
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

		checkLink(urls[0],visited[0],browser,iteration,fileOutput,types,pattern,MaxIteration)
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
		checkLink(urls[0],visited[0],browser,iteration,fileOutput,types,pattern, MaxIteration)
		output(visited,allLinks,brokenLinks, fileOutput,output_filename, images)

print "Running programm without parameters"
fileOutput = False
output_filename = None
types = ""
site = ""
pattern = "seafile.rlp.net"
MaxIteration = 9999
login(fileOutput,output_filename,types,pattern,site,MaxIteration)