# https://maps.googleapis.com/maps/api/geocode/xml?address=28+Yan+Kit+Road+Singapore&key=AIzaSyBRLOPPf6pFNtYlTW0wl93RBaW7udKbCCw

#!/usr/bin/env python
import urllib2
import urllib
import json
import pprint

# Use the json module to dump a dictionary to a string for posting.
data_string = urllib.quote(json.dumps({'id': 'data-explorer'}))

# blockstreetname = "510,ANG MO KIO AVENUE 8"
blockstreetname = "349,Hougang Ave"
blockstreetname = blockstreetname.replace(","," ")
blockstreetname = blockstreetname.replace(" ","+")
query = "+".join(["Block",blockstreetname,"Singapore"])
query = "Singapore"
url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + query + "&key=AIzaSyBRLOPPf6pFNtYlTW0wl93RBaW7udKbCCw"
long_name = "Block " + blockstreetname.split("+")[0]


print "query " + query

# Make the HTTP request.
# response = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address=Block+275C+Sengkang+Singapore&key=AIzaSyBRLOPPf6pFNtYlTW0wl93RBaW7udKbCCw',data_string)
response = urllib2.urlopen(url,data_string)
# assert response.code == 200

# Use the json module to load CKAN's response into a dictionary.
responsecontent = response.read()
print responsecontent
response_dict = json.loads(responsecontent)

# Check the contents of the response.
print response_dict['status']
result = response_dict['results']
# pprint.pprint(result)

# look for block location
block_location = None
for location in result:
    for component in location["address_components"]:
        if long_name in component["long_name"]:
            block_location = location
            break

pprint.pprint(block_location)


#
#                "lat" : 1.2754635,
#               "lng" : 103.8416603
#

#import urllib
#url = 'https://data.gov.sg/api/action/datastore_search?resource_id=8d2112ca-726e-4394-9b50-3cdf5404e790&limit=5&q=title:jones'
#fileobj = urllib.urlopen(url)
#print fileobj.read()
