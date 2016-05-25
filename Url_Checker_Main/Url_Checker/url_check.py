#!/usr/bin/python
import sys
from bs4 import BeautifulSoup as BS
import argparse
from seaserv import seafile_api
from .loginSelenium import loginSelenium

class Token:
	pass

#Defining variables 
output_filename = "visited.txt"
brokenImages = []
websiteImages =[]
newurl = ""
pdfs = []
brokenPDF = []
pattern = "seafile.rlp.net"
MaxIteration = 9999


#This method crawls through a site adn searches links. Takes the first link and follows them (number of Iterations). 
# After every link was visited crawler goes back to and searches for new links.
#Found links are stored in "url[]" and visited links are stored in "visited[]"

def main():

	if len(sys.argv) == 1:
		print "Running programm with Selenium"
		fileOutput = False
		output_filename = None
		types = ""
		site = ""
		pattern = "seafile.rlp.net"
		MaxIteration = 9999
		visited = []
		iteration = 0
		images = []
		allLinks = []
		brokenLinks = []
		notVisited = []
		brokenImages = []
		loginSelenium(notVisited,visited,iteration,fileOutput,output_filename,types,pattern,site,MaxIteration,images,allLinks,brokenLinks,brokenImages)

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
	parser.add_argument('-st', '--SeleniumTypes',	nargs = '*' ,		help='-st	: Same as ls, but with the option to search for image types')

	args = parser.parse_args()
	if args.iteration:
		print "Running programm with Selenium and MaxIteration %d"%(args.iteration)
		fileOutput = False
		output_filename = None
		types = ""
		site = ""
		pattern = "seafile.rlp.net"
		MaxIteration = args.iteration
		visited = []
		iteration = 0
		images = []
		allLinks = []
		brokenLinks = []
		notVisited = []
		brokenImages = []
		loginSelenium(notVisited,visited,iteration,fileOutput,output_filename,types,pattern,site,MaxIteration,images,allLinks,brokenLinks,brokenImages)
"""
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

	

	if args.SeleniumTypes:
		types = args.SeleniumTypes
		print "Running programm with Selenium"
		fileOutput = False
		output_filename = None
		site = ""
		pattern = "seafile.rlp.net"
		MaxIteration = 9999
		loginSelenium(fileOutput,output_filename,types,pattern,site,MaxIteration)
"""