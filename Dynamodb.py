from Place import *
import boto3
from boto3.dynamodb import *
from boto3.dynamodb.table import *
from boto3.dynamodb.conditions import Key, Attr
from GeoHash import *
from bitarray import bitarray
import traceback
from haversine import *


def insertPlaces(placelist, dynamodb):
    places = dynamodb.Table('places')
    try:
        with places.batch_writer() as batch:

            for place in placelist:
                batch.put_item(
                    Item={
                        'lat': place.getLatitude(),
                        'geohash': geoHash(place.getLat(), place.getLng()).to01(),
                        'lng': place.getLongitude(),
                        'place_id': place.getPlaceId(),
                        'name': place.getName(),
                        'restaurant': place.isRestaurant(),
                        'casino': place.isCasino(),
                        'liquor_store': place.isLiquorStore()

                    }
                )
        return True
    except:
        traceback.print_exc()
        print("Error occurred adding places data to table")
        return False



def retrievePlaces(dynamodb, lat, lng, types):
    places = dynamodb.Table('places')
    geoHashes = adjacentHashes(geoHash(lat, lng))
    if len(types)==0:
        return []
    result = []
    filter = None
    if len(types)==1:
        filter = Attr(types[0]).eq(True)
    elif len(types)==2:
        filter = Attr(types[0]).eq(True) | Attr(types[1]).eq(True)
    elif len(types)==3:
        filter = Attr(types[0]).eq(True) | Attr(types[1]).eq(True) | Attr(types[2]).eq(True)
    for hash in geoHashes:

        response = places.query(
            KeyConditionExpression = Key('geohash').eq(hash.to01()),
            FilterExpression = filter
        )
        items = response['Items']
        result += items
        print(items)
    return __placeResultToDict(result)

def __placeResultToDict(placeresult):
    places = []
    for place in placeresult:
        dict = {
            'lat': float(place['lat']),
            'lng': float(place['lng']),
            'name': place['name'],
            'restaurant': place['restaurant'],
            'casino': place['casino'],
            'liquor_store': place['liquor_store']
        }
        places.append(dict)
    return places



def insertRequest(dynamodb, lat, lng, type, radius):
    try:
        hash = geoHash(lat, lng, length=17)
        requests = dynamodb.Table('requests')
        requests.put_item(
            Item = {
                'geohash': hash.to01(),
                'lat': Decimal(str(lat)),
                'lng': Decimal(str(lng)),
                'type': type,
                'radius': Decimal(str(radius)),
                'unique': str(lat)+str(lng)+type+str(radius)
            }
        )
        return True
    except:
        traceback.print_exc()
        print("Error occurred inserting Request to table")
        return False



def whichTypesToRequestGoogle(dynamodb, lat, lng, types):
    requests = dynamodb.Table('requests')
    geohashes = adjacentHashes(geoHash(lat, lng, length=17))
    result = []
    for hash in geohashes:
        response = requests.query(

            KeyConditionExpression = Key('geohash').eq(hash.to01())
        )
        items = response['Items']
        result += items
    resultTypes = types.copy()
    if len(result)!=0:
        for request in result:
            requestlat = request['lat']
            requestlng = request['lng']
            type = request['type']
            radius = request['radius']
            if type in resultTypes:
                distance = haversine((lat, lng), (requestlat, requestlng))
                if (distance/float(radius))<=.8:
                    resultTypes.remove(type)
    return resultTypes