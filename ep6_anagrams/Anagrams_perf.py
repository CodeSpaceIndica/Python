import sys
import time

def findAnagram(aWord) :
    if( len(aWord) == 2 ) :
        newWords = []
        newWords.append( aWord[0] + aWord[1] )
        newWords.append( aWord[1] + aWord[0] )
        return newWords
    
    newWords = []
    for i in range( len(aWord) ) :
        firstLetter = aWord[i]
        rest = ""
        for j in range( len(aWord) ) :
            if( i != j ) :
                rest += aWord[j]

        returnedWords = findAnagram(rest)
        for retWord in returnedWords :
            allLengthWords.append( retWord )
            newWords.append(firstLetter + retWord)

    return newWords

def filterWords(aWord) :
    if aWord in allWords :
        return True
    return False

if ( len(sys.argv) < 2 ) :
    print("Require a parameter. Parameter can be any word")
    sys.exit(0)

text = sys.argv[1]
text = text.lower()

allLengthWords = []

startTime = time.time_ns()

results = findAnagram(text)
allLengthWords = allLengthWords + results
endTime = time.time_ns()

#print(results)
#print(allLengthWords)
timeTakenNS = endTime - startTime
timeTakenMS = timeTakenNS/1000000
print("**** It took", timeTakenMS, "milliseconds to find all anagrams")

print("Results had", len(results), "words of the same length")
print("Results had", len(allLengthWords), "words in total")
print("")

startTime = time.time_ns()
allLengthWordsSet = set(allLengthWords)
endTime = time.time_ns()
timeTakenNS = endTime - startTime
timeTakenMS = timeTakenNS/1000000
print("**** It took", timeTakenMS, "milliseconds to remove duplicates")
print("After removing duplicates, results had", len(allLengthWordsSet), "words of all lengths")
print("")

iFile = open("allwords.txt", "r")
line = iFile.readline()
allWords = line.split(",")
iFile.close()

#englishWords = list( filter(filterWords, allLengthWords) )
#print("There are", len(englishWords), "real English words. They are", englishWords)
startTime = time.time_ns()
englishWords = []
for realWord in allWords :
    if realWord in allLengthWordsSet :
        englishWords.append(realWord)
endTime = time.time_ns()
timeTakenNS = endTime - startTime
timeTakenMS = timeTakenNS/1000000
print("**** It took", timeTakenMS, "milliseconds to filter words.")
print("There are", len(englishWords), "real English words. They are", englishWords)