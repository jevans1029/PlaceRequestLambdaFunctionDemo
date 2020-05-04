import requests
from Place import *
from datetime import datetime

apikey = "xxxxxxxxxxxxxxxxxxxxxxx"

##Main function that calls the other functions
# uses formURL to form the request then passes json to getplaces then
#
def requestNearbyPlaces(lat, lng, type):
    assert (-90.0 <= lat <= 90.0)
    assert (-180.0 <= lng <= 180.0)
    response = requests.get(__formURL(lat, lng, type))
    json = response.json()
    placelist, radius = __getPlaces(json, (lat, lng))

    return placelist, radius



def __formURL(lat, lng, type):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    url += "location={},{}&".format(lat, lng)
    url += "radius=50000&"
    url += "type={}&".format(type)
    url += "key={}".format(apikey)
    return url

def __getPlaces(response_json, gps):
    response_result = response_json['results']
    distance = 0



    placelist = []
    if len(response_result) == 0:
        return placelist, 50000.0
    for place in response_result:
        geometry = place['geometry']
        location = geometry['location']
        lat = location ['lat']
        lng = location ['lng']
        km = haversine(gps, (lat, lng))
        if km > distance:
            distance = km
        name = place['name']
        placeId = place['place_id']
        restaurant = "restaurant" in place['types']
        casino = "casino" in place['types']
        liquor = "liquor_store" in place['types']
        placelist.append(Place(lat, lng, name, placeId, buildStringFromDatetime(), restaurant, casino, liquor))
    return placelist, distance


def buildStringFromDatetime():
    date = datetime.today()
    string = "{}-{}-{}".format(date.year, date.month, date.day)
    return string


if __name__=='__main__':
    requestNearbyPlaces(45.74, -90.01, "restaurant")