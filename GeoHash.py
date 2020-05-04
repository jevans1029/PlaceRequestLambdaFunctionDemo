from bitarray import bitarray
from bitarray import test

def geoHash(lat, lng, length=19):
    latrange = [-90.0, 90.0]
    lngrange = [-180.0, 180.0]
    bits = bitarray(length)
    for index in range(length):
        #is even
        if index % 2 == 0:
            lngdiff = lngrange[1] - lngrange[0]
            midpoint = lngrange[1]-(lngdiff/2.0)
            if lng <= midpoint:
                bits[index] = False
                lngrange[1] = midpoint
            else:
                bits[index] = True
                lngrange[0] = midpoint
        else:
            latdiff = latrange[1] - latrange [0]
            midpoint = latrange[1] - (latdiff/2.0)
            if lat <= midpoint:
                bits[index] = False
                latrange[1] = midpoint
            else:
                bits[index] = True
                latrange[0] = midpoint
        #print(bits.to01())
    #print(bits.to01())
    return bits



def gpsFromHash(string01):
    bits = bitarray(string01)
    latrange = [-90.0, 90.0]
    lngrange = [-180.0, 180.0]
    for index in range(bits.length()):
        # is even
        if index % 2 == 0:
            lngdiff = lngrange[1] - lngrange[0]
            lngmidpoint = lngrange[1] - (lngdiff / 2.0)
            if bits[index] == False:
                lngrange[1] = lngmidpoint
            else:
                lngrange[0] = lngmidpoint
        else:
            latdiff = latrange[1] - latrange[0]
            latmidpoint = latrange[1] - (latdiff / 2.0)
            if bits[index] == False:
                latrange[1] = latmidpoint
            else:
                latrange[0] = latmidpoint
    return (latrange, lngrange)



#
def __calculateAdjacent(bits: bitarray, type):

    positive = bits.copy()
    negative = bits.copy()
    length = bits.length()
    index = -1
    count = bits.count()

    carrySubtract = True
    carryAdd = True
    if count == length and type == 'lat':
        carryAdd = False
    elif count == 0 and type=='lat':
        carrySubtract = False

    while (carrySubtract or carryAdd) and abs(index)<=length:
        value = bits[index]
        if carrySubtract:
            if value:
                negative[index] = False
                carrySubtract = False
            else:
                negative[index] = True
        if carryAdd:
            if value:
                positive[index] = False
            else:
                positive[index] = True
                carryAdd = False
        index += -1
    return negative, positive

#parses a bitarray and returns two new bitarrays one for latitudes, one for longitudes
def __splitBits(bits: bitarray):
    lats = bitarray()
    lngs = bitarray()
    for index in range(bits.length()):
        if index % 2 == 0:
            lngs.append(bits[index])
        else:
            lats.append(bits[index])
    return (lngs, lats)


def __zipBits(lng: bitarray, lat: bitarray):
    latindex = 0
    lngindex = 0
    length = lng.length() + lat.length()
    bits = bitarray(length)

    for index in range(length):
        if index % 2 ==0:
            bits[index] = lng[lngindex]
            lngindex += 1
        else:
            bits[index] = lat[latindex]
            latindex += 1
    return bits


#takes the geohash of the original point as the parameter
def adjacentHashes(bits: bitarray):
    split = __splitBits(bits)
    lng = split[0]
    lat = split[1]
    toplat, bottomlat = __calculateAdjacent(lat, 'lat')
    leftlng, rightlng = __calculateAdjacent(lng, 'lng')
    left = __zipBits(leftlng, lat)
    right = __zipBits(rightlng, lat)
    top = __zipBits(lng, toplat)
    bottom = __zipBits(lng, bottomlat)
    topleft = __zipBits(leftlng, toplat)
    topright = __zipBits(rightlng, toplat)
    bottomleft = __zipBits(leftlng, bottomlat)
    bottomright = __zipBits(rightlng, bottomlat)
    return [bits, left, right, top, bottom, topleft, topright, bottomleft, bottomright]

def testGeoHashes(lat, lng):
    for gps in gpscoords:
        hash = geoHash(gps[0], gps[1])
        gpsresult = gpsFromHash(hash.to01())
        print("gps:" + str(gps) + "range:" + str(gpsresult))
        assert(gpsresult[0][0]<= gps[0]<=gpsresult[0][1])
        assert(gpsresult[1][0]<= gps[1] <= gpsresult[1][1])
    geohashes = adjacentHashes(geoHash(lat, lng))
    for hash in geohashes:
        print(hash.to01())


gpscoords = [(51.2, 102.5), (0.0, 90.0), (-89.9, 179.9), (89.9, -179.9), (89.9, 0.0)]



if __name__=='__main__':
    testGeoHashes(45.74, -90.0)

