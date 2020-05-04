import requests
url = "https://8b6zfwmnz4.execute-api.us-east-2.amazonaws.com/teststage?"
POSSIBLE_TYPES = ['casino', 'restaurant', 'liquor_store']
key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

def apiRequest(lat, lng, types):
    r = requests.get(__formURL(url, lat, lng, types), headers = {'X-API-Key': key})
    json = r.json()
    for place in json['places']:
        print(place)
    print(json['length'])

def __formURL(url, lat, lng, types):
    url += 'lat={}&'.format(lat)
    url += 'lng={}&'.format(lng)
    for type in POSSIBLE_TYPES:
        if type in types:
            url+= '{}=true&'.format(type)
        else:
            url += '{}=false&'.format(type)
    url = url[:-1]
    return url



if __name__== '__main__':
    apiRequest(42.00, -88.0, ['restaurant', 'liquor_store'])