#!/usr/bin/env python
import urllib2
import urllib
import json
import pprint
from basics import *


def getgeoloc(block,streetname):
    # Use the json module to dump a dictionary to a string for posting.
    data_string = urllib.quote(json.dumps({'id': 'data-explorer'}))

    # blockstreetname = "510,ANG MO KIO AVENUE 8"
    # blockstreetname = "349,Hougang Ave"
    blockstreetnameadd  = streetname.replace(" ","+")
    query = "+".join(["Block",block,"HDB",blockstreetnameadd,"Singapore"])
    # query = "Changsha+China"
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + query + "&key=AIzaSyBRLOPPf6pFNtYlTW0wl93RBaW7udKbCCw"
    long_name  = "Block " + block
    long_name2 = "Block " + block.lower()


    print "query " + query + " long name " + long_name

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
            if long_name in component["long_name"] or long_name2 in component["long_name"]:
                block_location = location
                break

    # if block_location == None:
    #     if len(result) == 1:
    #         location = result[0]
    #         block_location = location


    # pprint.pprint(block_location)

    if block_location != None:
        if "geometry" in block_location:
            if "bounds" in block_location["geometry"]:
                bounds = block_location["geometry"]["bounds"]
                p1 = bounds["northeast"]
                p2 = bounds["southwest"]
                coords = []
                for p in [p1,p2]:
                    coords = coords + [p["lat"],p["lng"]]
                return (coords,1)
            else:
                 if "location" in block_location["geometry"]:
                     p = block_location["geometry"]["location"]
                     coords = [p["lat"],p["lng"]]
                     r = 0.0001
                     coords = [coords[0] - r, coords[1] - r, coords[0] + r, coords[1] + r]
                     return (coords,1)
    else:
        if len(result) == 1:
             location = result[0]
             block_location = location  
             if "geometry" in block_location:
                 if "location" in block_location["geometry"]:
                     p = block_location["geometry"]["location"]
                     coords = [p["lat"],p["lng"]]
                     r = 0.0001
                     coords = [coords[0] - r, coords[1] - r, coords[0] + r, coords[1] + r]
                     return (coords,2)
    return (None,0)


def test():
    coords = getgeoloc("510","ANG MO KIO AVE 8")
    if coords == None:
        puts("no coords")
    else:
        puts(coords)

# test()
