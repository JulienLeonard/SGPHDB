from geolocutils import *
from basics import *

filepath = "resaleflatprices.csv"
content = ""
with open(filepath, 'r') as content_file:
    content = content_file.read()

geolocs = {}
maxnqueries = 1000
nqueries = 0

for line in content.split("\n")[1:]:
    # print line.split(",")
    (month,town,flat_type,block,street_name,storey_range,floor_area_sqm,flat_model,lease_commence_date,resale_price) = line.split(",")
    blockadress =  block + " " + street_name 
    if not blockadress in geolocs:
        coords = getgeoloc(blockadress)
        puts("adress",blockadress,"coords",coords)
        geolocs[blockadress] = coords
        nqueries += 1
        if nqueries > maxnqueries:
            break


with open("viewtemplate.html", 'r') as content_file:
    template = content_file.read()

COORDS = []
for key in geolocs:
    if geolocs[key] != None:
        COORDS.append("[" + ",".join([str(c) for c in geolocs[key]]) + "]")
COORDS = "[" + ",".join(COORDS) + "]"

content = template.replace("%COORDS%",COORDS)
file = open("try.html", "w")
file.write(content)
file.close()
