
from bs4 import BeautifulSoup as BS4
import requests
import time
from selenium.webdriver.common.action_chains import ActionChains as AC
import urlparse
import urllib2
from .output import output
import socket
import httplib

'''
function(verbleibendeLinks:Array, besuchteLinks:Array):
    aktuellerLink = verbleibendeLinks.pop()
    ...
    besuchteLinks.append(xyz)
    
    if verbleibendeLinks != leer:
        return function(verbleibendeLinks, besuchteLinks)

    else verbleibendeLinks == leer:
        return besuchteLinks

'''
def checkLinkSelenium(notVisited,visited,browser,iteration,fileOutput,output_filename,types,pattern, MaxIteration,images,allLinks,brokenLinks,brokenImages):
    # Set the startingpoint for the spider and initialize 
    # the a mechanize browser object
    # Since the amount of urls in the list is dynamic
    #   we just let the spider go until some last url didn't
    #   have new ones on the webpage
    
    iteration = iteration +1
    img_counter = 0
    if fileOutput == False:
        print "*"*50
        print "Checkin site "+notVisited[0]
        print notVisited
    currentUrl = notVisited.pop(0)
    visited.append(currentUrl)
    browser.get(currentUrl)
    r = requests.head(currentUrl)

    if "text/html" in r.headers["content-type"]:
        #visited.append(currentUrl)
        time.sleep(3)
        #checking if content of page is clickable or/and enabled
        try:
            op_container = browser.find_element_by_class_name('op-container')
            hover = AC(browser).move_to_element(op_container)
            hover.perform()
            notification_bell = browser.find_element_by_class_name('sf2-icon-bell')
            hover = AC(browser).move_to_element(notification_bell)
            hover.perform()
            if(op_container.is_enabled() and op_container.is_displayed()):
                print "Hover objects are enabled (share, delete and more options)"
            else:
                print "Hover objects are missing"
            if(notification_bell.is_enabled() and notification_bell.is_displayed()):
                print "Notification Bell is clickable"
            else:
                print "Notification Bell is not clickable"
        except Exception:
            print "Element not found"

        html_source = browser.page_source   
        soup = BS4(html_source,'html.parser')  
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
                            #if fileOutput == False:
                                #print "found image: %s" %(img)
                                #print "image is available"
                            images.append(img)
                            img_counter +=1
                                
                        else:
                            #if fileOutput == False:
                                #print "found image: %s" %(img)
                                #print "image site is down"
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
                            
                        elif "http" not in img or "www." not in img:
                            #print img
                            parsedLink = urlparse.urlsplit(currentUrl)
                            #print parsedLink                           
                            img = parsedLink.scheme+"://"+parsedLink.netloc+"/"+img
                            #print img


                        r = requests.head(img)
                        if r.status_code == requests.codes.ok:
                            #if fileOutput == False:
                                #print "found image: %s" %(img)
                                #print "image is available"
                            images.append(img)
                            img_counter +=1                             
                        else:
                            #if fileOutput == False:
                                #print "found image: %s" %(img)
                                #print "image site is down"
                            brokenImages.append(img)
                            img_counter +=1
                    except requests.HTTPError, e:
                        print "HTTP ERROR %s occured" % e.code
                        brokenImages.append(img)
                        img_counter +=1
                    except (requests.exceptions.MissingSchema) as e:
                        print "Missing schema occured. status %s"%e
                        print e
                        brokenImages.append(img)
                        img_counter +=1
                
    #finding links on site via webdriver
    links = browser.find_elements_by_xpath("//*[@href]")
    for link in links:
        url = link.get_attribute("href")            
        try: 
            response = urllib2.urlopen(url, timeout=3)
            allLinks.append("Url: %s | HTTP Status Code: %d" %(url,response.code))
            if url not in notVisited and url not in visited and pattern in url and "accounts/logout/" not in url:
                #print "%s | %d"%(url,response.code)
                notVisited.append(url)
        except urllib2.HTTPError, e:
            print url +" ist nicht erreichbar!"
            print ('HTTPError = ' + str(e.code))
            brokenLinks.append("Url: %s | HTTP Status Code: %s" %(url,str(e.code)))
        except urllib2.URLError, e:
            print url +" ist nicht erreichbar!"
            print ('URLError = ' + str(e.reason))
            brokenLinks.append("Url: %s | HTTP Status Code: %s" %(url,str(e.reason)))
        except httplib.HTTPException, e:
            print url +" ist nicht erreichbar!"
            print ('HTTPException = ' + str(e.reason))
            brokenLinks.append("Url: %s | HTTP Status Code: %s" %(url,str(e.reason)))
        except Exception:
            import traceback
            print url +" ist nicht erreichbar!"
            print ('generic exception: ' + traceback.format_exc())
            brokenLinks.append("Url: %s | HTTP Status Code: %s" %(url,traceback.format_exc()))
    if iteration <= MaxIteration:
        if len(notVisited) >= 0:
            print len(notVisited)
            return checkLinkSelenium(notVisited,visited,browser,iteration,fileOutput,output_filename,types,pattern, MaxIteration,images,allLinks,brokenLinks,brokenImages)
    if fileOutput == False:
        print "*"*50
        print "Number of images on this site %d"%(img_counter)
        print "Number of images: %d"%(len(images))
        
        
    print "iteration number: %d" %(iteration)
    output(visited,allLinks,brokenLinks,fileOutput,output_filename, images,brokenImages)
    return visited