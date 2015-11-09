from geolocutils import *
from basics import *
from geoloccache import *

filepath = "resaleflatprices.csv"
content = ""
with open(filepath, 'r') as content_file:
    content = content_file.read()


maxnqueries = 50000
nqueries = 0
nlines = 0

blockadresses  ={}

for line in content.split("\n")[1:]:
    (month,town,flat_type,block,street_name,storey_range,floor_area_sqm,flat_model,lease_commence_date,resale_price) = line.split(",")
    block = block.strip()
    street_name = street_name.strip()
    blockadress =  (block + " " + street_name).strip()
    if not blockadress in blockadresses:
        blockadresses[blockadress] = 0
    blockadresses[blockadress] += 1    

puts("nblockadresses",len(blockadresses.keys()))
sortlist = [(blockadresses[blockadress],blockadress) for blockadress in blockadresses]
sortlist.sort()
#for (n,adress) in sortlist:
#    puts("adress",adress,"n",n)



for line in content.split("\n")[1:]:
    puts("nline",nlines)
    nlines += 1
    # print line.split(",")
    (month,town,flat_type,block,street_name,storey_range,floor_area_sqm,flat_model,lease_commence_date,resale_price) = line.split(",")
    block = block.strip()
    street_name = street_name.strip()
    blockadress =  (block + " " + street_name).strip()
    if not blockadress in geolocs:
        coords = getgeoloc(block,street_name)
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

scache = []
for key in geolocs:
    if geolocs[key] != None:
        scache.append( "\"" + key.strip() + "\":" "[" + ",".join([str(c) for c in geolocs[key]]) + "]")

file = open("geoloccache.py", "w")
file.write("geolocs = {" + ",\n".join(scache) + "}")
file.close()


