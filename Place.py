from haversine import *
from decimal import *

class Place:

    def __init__(self, lat, lng, name: str, placeId, date, restaurant, casino, liquor_store):
        self.lat = lat
        self.lng = lng
        self.name = name.replace("'", "")
        self.restaurant = restaurant
        self.casino = casino
        self.liquor_store = liquor_store
        self.date = date
        self.placeId = placeId

    def getLatitude(self):
        return Decimal(str(self.lat))

    def getLongitude(self):
        return Decimal(str(self.lng))

    def getLat(self):
        return self.lat

    def getLng(self):
        return self.lng

    def getRoundedLng(self):
        return int(round(self.lng))

    def getName(self):
        return self.name

    def getPlaceId(self):
        return self.placeId

    def isRestaurant(self):
        return self.restaurant


    def isCasino(self):
        return self.casino



    def isLiquorStore(self):
        return self.liquor_store

    def getDate(self):
        return self.date

    def calcLatMEDIUMINT(self):
        mediumint = int(self.lat*10000)
        if mediumint>900000:
            mediumint = 900000
        elif mediumint<-900000:
            mediumint = -900000
        return mediumint

    def calcLngMEDIUMINT(self):
        mediumint = int(self.lng*10000)
        if mediumint>1800000:
            mediumint = 1800000
        elif mediumint<-1800000:
            mediumint = -1800000
        return mediumint

    def getDict(self):
        dict = {
            'lat': self.lat,
            'lng': self.lng,
            'name': self.name,
            'restaurant': self.restaurant,
            'casino': self.casino,
            'liquor_store': self.liquor_store
        }
        return dict

#(lat, lng)
def findRadius(gps, placelist):
    distance = 0
    if len(placelist)==0:
        return 50000.0
    for place in placelist:
        km = haversine(gps, (place.getLng(), place.getLng()))
        if km>distance:
            distance = km
    return distance


