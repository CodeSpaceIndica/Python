import urllib.request
import time
from html.parser import HTMLParser

urlTemplate = "https://results.eci.gov.in/ACTRENDS2020/ConstituencywiseS04{con}.htm?ac={con}"

partyData = []

class CSHTMLParser(HTMLParser) :
    isPartyNameTag = False
    votesDataCtr = 0

    partyName = ""

    def handle_starttag(self, tag, attrs):
        alignValue = ""
        styleValue = ""
        if( tag == "td" ) :
            for attr in attrs :
                if( attr[0] == "align" ) :
                    alignValue = attr[1]
                if( attr[0] == "style" ) :
                    styleValue = attr[1]
            if( alignValue == "left" and styleValue == "width:0%;font-weight:bold;") :
                self.isPartyNameTag = True
            if( alignValue == "right" and styleValue == "width:13%;font-weight:bold;") :
                self.votesDataCtr = self.votesDataCtr + 1

    def handle_data(self, data):
        if( self.isPartyNameTag ) :
            self.partyName = data
            self.isPartyNameTag = False
        if( self.votesDataCtr == 2 ) :
            partyData.append( self.partyName + "|" + data )
            self.votesDataCtr = 0

parser = CSHTMLParser()
with open("bihar_constituencies.txt") as fileObject:
    aLine = fileObject.readline()
    while aLine :
        aLine = aLine.strip()
        splitValues = aLine.split(",")
        conID = splitValues[0]
        conNm = splitValues[1]

        theURL = urlTemplate.format( con = conID )
        
        print("Hitting url :", theURL)
        urlObject = urllib.request.urlopen(theURL)
        fileContents = urlObject.read().decode("utf-8")
        parser.feed(fileContents)

        time.sleep(1)

        aLine = fileObject.readline()

#print(partyData)
with open("results_data.txt", "w") as resultsFileObj :
    for data in partyData :
        resultsFileObj.write(data + "\n")
