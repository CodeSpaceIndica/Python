#This file takes the new_allwords.txt file
#prepares the regex and creates a property 
#out of it. That way we can create a better 
#version of the program that might be a tad
#faster.

with open("new_allwords.txt") as fObj : 
    aLine = fObj.readline() 
    while aLine : 
        #Strip line of any white spaces including new keys
        aLine = aLine.strip() 
        #sort the word based on its alphabets
        arr = sorted(aLine) 
        #Create a regex pattern. In the following two lines the 
        #word is converted into a pattern that will look like this
        #A word "mask" will be converted to its key "akms" and 
        #that will converted to a regular expression pattern
        # [a-z]*a{1}[a-z]*k{1}[a-z]*m{1}[a-z]*s{1}[a-z]*
        regexPattern = r"{1}[a-z]*".join(arr) 
        regexPattern = "[a-z]*" + regexPattern + r"{1}[a-z]*" 
        #This pattern is matched agains the key
        print( regexPattern, end="" )
        print( "=", end="" )
        print( aLine )

        aLine = fObj.readline()

fObj.close()