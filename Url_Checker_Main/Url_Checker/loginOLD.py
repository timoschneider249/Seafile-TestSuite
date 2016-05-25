"""
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
        br.open("https://seafile.rlp.net/shib-login/?next=/") 
        br.select_form(nr=0)
        

        
        res = br.submit(name = "shib-login") 
        print res
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
        
""" 