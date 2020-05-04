import json
from GoogleRequest import *
import boto3
from boto3.dynamodb import *
from decimal import *
from Dynamodb import *
from bitarray import bitarray

POSSIBLE_TYPES = ('restaurant', 'casino', 'liquor_store')

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    lat = float(event['queryStringParameters']['lat'])
    lng = float(event['queryStringParameters']['lng'])
    types = []
    body = {}
    placesResult = []
    for type in POSSIBLE_TYPES:
        if event['queryStringParameters'][type] == 'true':
            types.append(type)
    googleTypes = whichTypesToRequestGoogle(dynamodb, lat, lng, types)
    for googletype in googleTypes:
        placelist, radius = requestNearbyPlaces(lat, lng, googletype)

        if insertPlaces(placelist, dynamodb):
            insertRequest(dynamodb, lat, lng, googletype, radius)
        for place in placelist:
            placesResult.append(place.getDict())
    typesToQuery = []
    for type in types:
        if type not in googleTypes:
            typesToQuery.append(type)
    placesResult += retrievePlaces(dynamodb, lat, lng, typesToQuery)
    out = {}
    headers = {}
    copy_headers = ('Accept', 'Content-Type')
    for h in copy_headers:
        if h in event['headers']:
            headers[h] = event['headers'][h]

    body['places'] = placesResult
    body['length'] = len(placesResult)
    out['headers'] = headers
    out["statusCode"] = 200
    out['isBase64Encoded'] = False
    out['body'] = json.dumps(body)
    return out


def testDynamo():
    dynamodb = boto3.resource('dynamodb')
    places = dynamodb.Table('places')
    print(places.creation_date_time)
    places.put_item(
        Item={
            'lat': Decimal('45.78'),
            'lng': Decimal('-90.0'),
            'name': 'place',
            'restaurant': True
        }
    )
    response = places.get_item(
        Key={
            'lat': Decimal('45.78'),
            'lng': Decimal('-90.0')
        }
    )
    item = response['Item']
    print(item)




if __name__=="__main__":
    placelist = requestNearbyPlaces(45.74, -90.0, "restaurant")


#dynamodb = boto3.resource('dynamodb')
#insertPlaces(placelist, dynamodb)
#retrievePlaces(dynamodb, 45.74, -90.0)




