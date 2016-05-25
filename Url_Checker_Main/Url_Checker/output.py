
def output(visited, allLinks, brokenLinks, fileOutput,output_filename, images,brokenImages):
    i = 0

    if fileOutput == False:
        print "*"*50
        print "visited" 
        for item in visited:
            print item
        print "*"*50
        print "all Links"   
        for item in allLinks:
            print item
        print "*"*50
        print "broken Links"    
        for item in brokenLinks:
            print item
        print "*"*50
        print "images"  
        for item in images:
            print item
        print "*"*50
        print "broken images" 
        for item in brokenImages:
            print item
        print "*"*50
        print "uniqueLinks"
        uniqueLinks = set(allLinks)
        for item in uniqueLinks:
            print item
        print "*"*50
        print "Total number of links found: %d"%len(allLinks)
        print "Total number of distinct links found: %d"%len(uniqueLinks)
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
        writeFile.write("<<<<Images>>>>\n\n")
        for item in images:
            i +=1
            writeFile.write("%d. %s \n"%(i,item))
        writeFile.close()