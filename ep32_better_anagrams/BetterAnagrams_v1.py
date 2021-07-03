#faster than V2
import sys
import re
import time

if ( len(sys.argv) < 2 ) : 
    print("Require a parameter. Parameter can be any word") 
    sys.exit(0)

startTime = time.time_ns()

text = sys.argv[1]
#Convert text to lower case
text = text.lower()
#Split the word into an array, sort it by alphabets and join it back.
#This becomes a key
#If the word was "alpha", then its key is "aahlp"
key = "".join(sorted(text))

#Get and store the length of the key before hand
textLen = len(key)

print(text, key, textLen)

cnt = 0
#Open a list of all the words in the english language.
with open("new_allwords.txt") as fObj : 
    aLine = fObj.readline() 
    while aLine : 
        #Strip line of any white spaces including new keys
        aLine = aLine.strip() 
        #Do regex comparison only if 
        #the length of the word is less than or equal to the Key
        if( len(aLine) <= textLen ) :
            #sort the word based on its alphabets
            arr = sorted(aLine) 
            #Do the regex comparison only if 
            #the first letter of the word appears in the key
            if arr[0] in key :
                #Create a regex pattern. In the following two lines the 
                #word is converted into a pattern that will look like this
                #A word "mask" will be converted to its key "akms" and 
                #that will converted to a regular expression pattern
                # [a-z]*a{1}[a-z]*k{1}[a-z]*m{1}[a-z]*s{1}[a-z]*
                regexPattern = r"{1}[a-z]*".join(arr) 
                regexPattern = "[a-z]*" + regexPattern + r"{1}[a-z]*" 
                #This pattern is matched agains the key
                match = re.match(regexPattern, key) 
                if match : 
                    print(aLine)
                    cnt = cnt + 1
        aLine = fObj.readline()

fObj.close()

endTime = time.time_ns()
timeTakenNS = endTime - startTime
timeTakenMS = timeTakenNS/1000000
print("**** It took", timeTakenMS, "milliseconds to find", cnt, "anagrams")