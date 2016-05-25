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

