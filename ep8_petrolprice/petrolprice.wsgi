import pymysql
import json

dbUserName = "fuel_user2"
dbPassword = "Fuel#11Master"
dbName     = "Petrol_Prices"
sqlQuery   = "select StationName, StationAddress, Petrol, Diesel, \
                PremiumPetrol, PremiumDiesel \
                from Historical h \
                where City=%s \
                and DateTime >= CURDATE()"

def application(environ, startResponse):

        dbConnection = pymysql.connect(host='localhost', 
                        user=dbUserName, 
                        passwd=dbPassword,
                        db=dbName)

        startResponse("200 OK", [("Content-type", "application/json")])

        requestURI = environ['REQUEST_URI']
        index = requestURI.rfind("/") + 1
        theCity = requestURI[index:]

        jsonReturnData = {"city": theCity}
        with dbConnection.cursor() as queryCursor :
            queryCursor.execute(sqlQuery, theCity)
            prices = []
            for resultRow in queryCursor :
                stationName = resultRow[0]
                stationAddr = resultRow[1]
                petrolPrice = resultRow[2]
                dieselPrice = resultRow[3]
                prmPetPrice = resultRow[4]
                prmDisPrice = resultRow[5]
                data = {"stationName": stationName, 
                    "stationAddr": stationAddr,
                    "petrolPrice": petrolPrice,
                    "dieselPrice": dieselPrice,
                    "prmPetPrice": prmPetPrice,
                    "prmDisPrice": prmDisPrice}
                prices.append(data)
                jsonReturnData["prices"] = prices

        jsonStr = json.dumps(jsonReturnData)

        return [bytes(jsonStr, "utf-8")]

