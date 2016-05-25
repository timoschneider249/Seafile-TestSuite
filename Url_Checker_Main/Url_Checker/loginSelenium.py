#-*- coding: utf-8 -*-

from .checkLinkSelenium import checkLinkSelenium

from selenium import webdriver
#from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

import time
from bs4 import BeautifulSoup as BS4

def loginSelenium(notVisited, visited,iteration,fileOutput,output_filename,types,pattern,site,MaxIteration,images,allLinks,brokenLinks,brokenImages):

    username = "timschne@uni-mainz.de"
    password = "Rbgt0757!"
    
    if site is "":
        url = "https://seafile.rlp.net/"

    browser = webdriver.Firefox()
    browser.get(url)
    local_input = browser.find_element_by_id("shib-login").click()
    uniMainz = browser.find_element_by_xpath('//div[contains(@onclick,"https://login.uni-mainz.de/adfs/services/trust")]')
    uniMainz.click()
    usernameId = browser.find_element_by_id("userNameInput")
    passwordId = browser.find_element_by_id("passwordInput")
    usernameId.send_keys(username) 
    passwordId.send_keys(password)
    login_attempt = browser.find_element_by_id("submitButton").click()
        
    notVisited.append(url)

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
    time.sleep(2)
    html_source = browser.page_source   
    soup = BS4(html_source,'html.parser')  

    login_check = soup.findAll('img',{'class':'avatar'}) 
        
    if not login_check:
        print "username or password incorrect"
        browser.quit()
        sys.exit(0) 
    else:
        print "Successfully logged in as %s" %username
    
    checkLinkSelenium(notVisited,visited,browser,iteration,fileOutput,output_filename,types,pattern,MaxIteration,images,allLinks,brokenLinks,brokenImages)
    



        
    """
    #Get origin_repo object
    #Get library ID from input
    origin_repo_id = "eb782297-bfd9-49c4-8f17-ea5c9e686a73"
    print "Repo_id: %s"%(origin_repo_id)
    origin_repo = seafile_api.get_repo(origin_repo_id)
    username = seafile_api.get_repo_owner(origin_repo_id)
    print "origin_repo_id: %s" %(origin_repo)
    print "username: %s" %(username)
    #Create a new library, set name, desc and owner
    new_repo_id = seafile_api.create_repo(name=origin_repo.name,
                                      desc=origin_repo.desc,
                                      username=username, passwd=None)
    #access_token = seafile_api.get_httpserver_access_token(origin_repo_id, 'dummy', 'view', username)
    #print "Access token: %"%(access_token)
        

    print "New Repo Id: %s"%(new_repo_id)
    print "*" * 60
    """
    browser.quit()