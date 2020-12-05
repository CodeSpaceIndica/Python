import requests
import time
import pymysql

iolServiceURL = "https://associates.indianoil.co.in/PumpLocator/NearLocations"
dbName = "Petrol_Prices"
uName = "fuel_user2"
psswd = "Fuel#11Master"
delay = 1 #Number of seconds

insertSQL = "insert into Historical \
    (DateTime, City, StationName, StationAddress, Petrol, Diesel, PremiumPetrol, PremiumDiesel) \
    values \
    (now(), %s, %s, %s, %s, %s, %s, %s)"

dbConnection = pymysql.connect(host='localhost', 
                        user=uName, 
                        passwd=psswd,
                        db=dbName)

with open("city_latlong.properties") as props:
    for aLine in props :
        if aLine.startswith("#") :
            continue

        aLine = aLine.strip()
        split1 = aLine.split("=")
        city = split1[0]
        latlong = split1[1]
        split2 = latlong.split(",")
        latitude  = split2[0]
        longitude = split2[1]

        print("Getting petrol prices for", city)

        postData = {"latitude": latitude, "longitude": longitude}

        petrolData = requests.post(iolServiceURL, data=postData)

        petrolData = petrolData.text
        petrolData = petrolData.strip()
        stationData = petrolData.split("|")
        for station in stationData :
            stationDetails = station.split(",")
            if len(stationDetails) > 1  :
                stationName = stationDetails[0]
                stationAddr = stationDetails[3]
                petrolPrice = float(stationDetails[25].strip())
                dieselPrice = float(stationDetails[26].strip())
                prmPetPrice = float(stationDetails[27].strip())
                prmDisPrice = float(stationDetails[28].strip())
                #print(petrolPrice, dieselPrice, prmPetPrice, prmDisPrice)
                with dbConnection.cursor() as insertCursor :
                    insertCursor.execute(insertSQL, (city, stationName, stationAddr, petrolPrice, dieselPrice, prmPetPrice, prmDisPrice))

        dbConnection.commit()
        print("done")

        #Sleep
        time.sleep(delay)

dbConnection.close()
print("Done Done.")