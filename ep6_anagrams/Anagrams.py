#A python program to find anagrams of a given word.
import sys

allLengthAnagrams = []

def findAnagrams(aWord) :
    anagrams = []
    if( len(aWord) == 2 ) :
        anagrams.append( aWord[0] + aWord[1] )
        anagrams.append( aWord[1] + aWord[0] )
        return anagrams

    for i in range(len(aWord)) :
        aLetter = aWord[i]
        restOfLetters = ""
        for j in range(len(aWord)) :
            if( i != j ) :
                restOfLetters = restOfLetters + aWord[j]
        anagramRest = findAnagrams(restOfLetters)
        for restWord in anagramRest :
            allLengthAnagrams.append(restWord)
            anagrams.append(aLetter + restWord)

    return anagrams

if( len(sys.argv) < 2 ) :
    print("How about a parameter there champ?")
    sys.exit(1)

aWord = sys.argv[1]

wordAnagrams = findAnagrams(aWord)
#print(wordAnagrams)
#print(allLengthAnagrams)
#print("There were", len(wordAnagrams), "found")

allLengthAnagrams = set(allLengthAnagrams)

allEnglishWords = []
with open("allwords.txt") as fIn:
    allEnglishWords = fIn.read().split(",")

englishAnagrams = []
for englishWord in allEnglishWords :
    if englishWord in allLengthAnagrams :
        englishAnagrams.append(englishWord)

print("Here is all english anagrams")
print(englishAnagrams)
