#slower than V1
import sys
import re
import time

if ( len(sys.argv) < 2 ) : 
    print("Require a parameter. Parameter can be any word") 
    sys.exit(0)

startTime = time.time_ns()

text = sys.argv[1]
text = text.lower()
key = "".join(sorted(text))
textLen = len(key)

print(text, key, textLen)

allWords = []
with open("new_allwords.txt") as fObj : 
    aLine = fObj.readline() 
    while aLine : 
        aLine = aLine.strip() 
        if( len(aLine) <= textLen ) : 
            allWords.append(aLine)
        aLine = fObj.readline()

fObj.close()

for aLine in allWords : 
    arr = sorted(aLine) 
    regexPattern = r"{1}[a-z]*".join(arr) 
    regexPattern = "[a-z]*" + regexPattern + r"{1}[a-z]*" 
    match = re.match(regexPattern, key) 
    if match : 
        print(aLine)

endTime = time.time_ns()
timeTakenNS = endTime - startTime
timeTakenMS = timeTakenNS/1000000

print("**** It took", timeTakenMS, "milliseconds to find all anagrams")