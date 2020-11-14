
partyWithSeats = ["All India Majlis-E-Ittehadul Muslimeen", "Bahujan Samaj Party", 
                "Bharatiya Janata Party", "Communist Party of India", 
                "Communist Party of India  (Marxist-Leninist)  (Liberation)",
                "Communist Party of India  (Marxist)",
                "Hindustani Awam Morcha (Secular)",
                "Independent", "Indian National Congress", "Janata Dal (United)",
                "Lok Jan Shakti Party", "Rashtriya Janata Dal", "Vikassheel Insaan Party"]

partyAndCounts = {}
allPartyCounts = {}

with open("results_data.txt") as resFileObj :
    aLine = resFileObj.readline()

    while aLine :
        aLine = aLine.strip()
        splitData = aLine.split("|")
        partyName = splitData[0]
        partyVots = splitData[1]

        theDigit = partyVots[0]
        #theDigit = partyVots[-2] + partyVots[-1]

        if( partyName in partyAndCounts) :
            countValues = partyAndCounts[partyName]
            if( theDigit in countValues ) :
                count = countValues[theDigit]
                count = count + 1
                countValues[theDigit] = count
            else :
                countValues[theDigit] = 1
        else :
            partyAndCounts[partyName] = {theDigit: 1}

        if theDigit in allPartyCounts :
            count = allPartyCounts[theDigit]
            count = count + 1
            allPartyCounts[theDigit] = count
        else :
            allPartyCounts[theDigit] = 1

        aLine = resFileObj.readline()

#for partyName in sorted(partyAndCounts.keys()) :
for partyName in partyWithSeats:
    print(partyName)
    countValues = partyAndCounts[partyName]
    for key in sorted(countValues.keys()) :
        print(key + "\t" + str(countValues[key]))

print("---------------")

for key in sorted(allPartyCounts.keys()) :
    print(key + "\t" + str(allPartyCounts[key]))
