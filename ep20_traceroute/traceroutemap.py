import sys
import ipaddress
import configparser
import pymysql
import math
from PIL import Image, ImageDraw
from icmplib import ping, traceroute, Host, Hop

#Define the size of the map
mapWidth = 2521
mapHeight = 1260

#Convert float latitude and longitude to X and Y pixels on the map
def latLongToXY(latitude, longitude) :
    x = (longitude+180)*(mapWidth/360)

    latRad = latitude*math.pi/180
    mercN = math.log( math.tan( (math.pi/4)+(latRad/2) ) )
    y = (mapHeight/2)-(mapWidth*mercN/(2*math.pi))

    return {"x":x, "y": y}

#Read parameter from command line
if len(sys.argv) < 2 :
    print("Need a website as parameter")
    sys.exit(0)

address = sys.argv[1]

#Parse the .ini file
print("Connecting to DB...")
config = configparser.ConfigParser()
config.read("database.ini")

#and assign the values to variables.
host   = config["DatabaseDetails"]["ServerHost"]
dbname = config["DatabaseDetails"]["DBName"]
uname  = config["DatabaseDetails"]["UserName"]
psswrd = config["DatabaseDetails"]["Password"]

#Connect the database
dbConnection = pymysql.connect(host=host,
                                user=uname,
                                passwd=psswrd,
                                db=dbname)

#Open image and keep in memory
print("Opening Image...")
image = Image.open("World Map.png")
drawer = ImageDraw.Draw(image)

#Performs actual trace route over ICMP
print("Performing TraceRoute...")
hops = traceroute(address, count=2, interval=0.05, timeout=2, first_hop=1, max_hops=30, source=None, fast=False)

#A query to fetch latitude and longitude.
#This can be replaced by a webservice call as well
latLongQuery = "select latitude, longitude from ip_location il where %s between start_ip  and end_ip"

pX = 0
pY = 0
for hop in hops :
    ipAddrStr = hop.address
    ipAddr = ipaddress.IPv4Address(ipAddrStr)
    ipAddrLong = int(ipAddr) #Convert IP Address to LONG
    #print("Querying", hop.address, hop.avg_rtt, hop.distance, ipAddrLong)
    print("Querying " + hop.address + "(" + str(ipAddrLong) + ")", end=" ")
    lat = 0
    lng = 0
    with dbConnection.cursor() as cursor :
        cursor.execute(latLongQuery, ipAddrLong) #Execute query
        rows = cursor.fetchall()
        for row in rows:
            lat = float(row[0])  #Latitude
            lng = float(row[1])  #Longitude
    if lat != 0 and lng != 0 :
        xyLoc = latLongToXY(lat, lng) #To XY co-ords on screen
        x = xyLoc["x"]
        y = xyLoc["y"]
        print("Lat-Long = " + str(lat) + "," + str(lng) + "(" + str(x) + "," + str(y) + ")")
        #Draw a line on the image.
        if pX != 0 and pY != 0 :
            drawer.line(xy=(pX, pY, x, y), fill=(255, 0, 0), width=3)
        pX = x
        pY = y

#Close DB connection
dbConnection.close()

#Show image
image.show()
