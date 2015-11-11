from geolocutils import *
from basics import *
from geoloccache import *

def dumpmap(geolocs,leases):

    with open("viewtemplate.html", 'r') as content_file:
        template = content_file.read()

    leaserange = lrange(leases.values()) 
    puts("leaserange",leaserange)

    HDBS = []
    for key in geolocs:
        if geolocs[key] != None:
            HDB = "{coords: [" + ",".join([str(c) for c in geolocs[key]]) + "],"
            if key in leases:
                b = int(255.0 * (1.0 - abscissa(leaserange,leases[key])))
                r = 255 - b
                HDB = HDB + "color: rgbToHex(" + str(r) + ",0," + str(b) + "), lease: " + str(int(leases[key])) + "}"
            else:
                HDB = HDB + "color: rgbToHex(125,125,125), lease: " + str(int(leaserange[0])) + "}"
            HDBS.append(HDB)
            
    HDBS = "[" + ",".join(HDBS) + "]"

    content = template.replace("%HDBS%",HDBS).replace("%RANGEMIN%",str(int(leaserange[0]))).replace("%RANGEMAX%",str(int(leaserange[1])))
    file = open("try.html", "w")
    file.write(content)
    file.close()

def dumpcache(geolocs):
    scache = []
    for key in geolocs:
        if geolocs[key] != None:
            scache.append( "\"" + key.strip() + "\":" "[" + ",".join([str(c) for c in geolocs[key]]) + "]")

    file = open("geoloccache.py", "w")
    file.write("geolocs = {" + ",\n".join(scache) + "}")
    file.close()


filepath = "resaleflatprices.csv"
content = ""
with open(filepath, 'r') as content_file:
    content = content_file.read()


maxnqueries = 0
nqueries = 0
nlines = 0

blockadresses  ={}
leases = {}

for line in content.split("\n")[20000:]:
    (month,town,flat_type,block,street_name,storey_range,floor_area_sqm,flat_model,lease_commence_date,resale_price) = line.split(",")
    block = block.strip()
    street_name = street_name.strip()
    blockadress =  (block + " " + street_name).strip()
    if not blockadress in blockadresses:
        blockadresses[blockadress] = 0
    blockadresses[blockadress] += 1    
    leases[blockadress] = float(lease_commence_date.strip())
    # leases[blockadress] = float(floor_area_sqm.strip())

puts("nblockadresses",len(blockadresses.keys()))
sortlist = [(blockadresses[blockadress],blockadress) for blockadress in blockadresses]
sortlist.sort()
#for (n,adress) in sortlist:
#    puts("adress",adress,"n",n)

dumpcache(geolocs)
dumpmap(geolocs,leases)


for line in content.split("\n")[1000:]:
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
        if not coords == None:
            dumpcache(geolocs)
            dumpmap(geolocs,leases)
        nqueries += 1
        if nqueries > maxnqueries:
            break



