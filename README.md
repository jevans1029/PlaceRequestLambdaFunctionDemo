# PlaceRequestLambdaFunctionDemo

This is a lambda function for caching google places data. 

A mobile or web application can send an API request to this lambda function with the current gps coordinates of the user and the type of places that the application is looking for and the lambda function will then send a request to google for nearby places matching the requested type of place. The lambda function will then calculate the geohash of the returned places and save the details in a dynamodb database. The geohash algorithm is described below and is used as the partition key for the dynamodb database. The gps coordinates of the user and the time and date of the request are then saved in the dynamodb database to avoid requesting the data from google again until the specified expiration time has passed.

#Geohash

The geohash algorithm converts a set of latitude and longitude coordinates to a binary array. The array defines what bounded square the gps coordinates are located in on the globe. How big the squares are depends on how long the binary is. 

The binary array is built by starting by looking at the longitude value and asking is it greater than or less than 0. If it is greater than, the value will be 1 and if less than it will be 0. Then next index of the binary array does the same with the latitude. The next index checks if the longitude is above or below the midpoint of 0 and 180 or 0 and -180 depending on what range the longitude is in. This process repeats for the length of the array, alternating between longitude and latitude. This results in a narrowing square the gps coordinates are located in. 

#Consecutive Requests

After data is cached in the database for a particular area the lambda function will request the data from the database instead of making a new request to google. It finds what geohash square the user's gps coordinates are in and then pulls the requested data from the adjacent geohash squares. In order to size the geohash squares correctly, the geohash length is set to 17 bits long. 
