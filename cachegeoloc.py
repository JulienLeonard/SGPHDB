from geolocutils import *
from basics import *
# define geolocs
from geoloccache import *

def dumpmaplease(geolocs,HDBs):

    with open("viewtemplate.html", 'r') as content_file:
        template = content_file.read()

    leases     = {cHDB.blockadress(): cHDB.lease for cHDB in HDBs}
    leaserange = lrange([float(lease) for lease in leases.values()]) 

    puts("leaserange",leaserange)

    HDBS = []
    for blockadress in leases.keys():
        lease = leases[blockadress]
        if blockadress in geolocs:
            (HDBgeoloc,reliability) = geolocs[blockadress]
            if HDBgeoloc != None:
                HDB = "{coords: [" + ",".join([str(c) for c in HDBgeoloc]) + "],adress: \"" + blockadress +  "\","
                b = int(255.0 * (1.0 - abscissa(leaserange,float(lease))))
                r = 255 - b
                HDB = HDB + "color: rgbToHex(" + str(r) + ",0," + str(b) + "), lease: " + str(int(lease)) + "}"
                #else:
                #    puts("error: adress " + key + " no lease")
                #    HDB = HDB + "color: rgbToHex(125,125,125), lease: " + str(int(leaserange[0])) + "}"
                HDBS.append(HDB)
            
    HDBS = "[" + ",".join(HDBS) + "]"

    content = template.replace("%HDBS%",HDBS).replace("%RANGEMIN%",str(int(leaserange[0]))).replace("%RANGEMAX%",str(int(leaserange[1])))
    file = open("try.html", "w")
    file.write(content)
    file.close()

def dumpmapsqm(geolocs,HDBs):

    with open("viewtemplate.html", 'r') as content_file:
        template = content_file.read()

    sqms     = {cHDB.blockadress(): [] for cHDB in HDBs}
    for cHDB in HDBs:
        sqms[cHDB.blockadress()] = sqms[cHDB.blockadress()] +[cHDB.floor_area_sqm]
    sqms     = {key: lmax(sqms[key]) for key in sqms.keys()}
    sqmrange = lrange([float(sqm) for sqm in sqms.values()]) 

    puts("sqmrange",sqmrange)

    HDBS = []
    for blockadress in sqms.keys():
        sqm = sqms[blockadress]
        if blockadress in geolocs:
            (HDBgeoloc,reliability) = geolocs[blockadress]
            if HDBgeoloc != None:
                HDB = "{coords: [" + ",".join([str(c) for c in HDBgeoloc]) + "],"
                b = int(255.0 * (1.0 - abscissa(sqmrange,float(sqm))))
                r = 255 - b
                HDB = HDB + "color: rgbToHex(" + str(r) + ",0," + str(b) + "), lease: " + str(int(sqm)) + "}"
                #else:
                #    puts("error: adress " + key + " no sqm")
                #    HDB = HDB + "color: rgbToHex(125,125,125), sqm: " + str(int(sqmrange[0])) + "}"
                HDBS.append(HDB)
            
    HDBS = "[" + ",".join(HDBS) + "]"

    content = template.replace("%HDBS%",HDBS).replace("%RANGEMIN%",str(int(sqmrange[0]))).replace("%RANGEMAX%",str(int(sqmrange[1])))
    file = open("try.html", "w")
    file.write(content)
    file.close()


def dumpmappricepersqm(geolocs,HDBs):

    with open("viewtemplate.html", 'r') as content_file:
        template = content_file.read()

    leaserange = lrange([cBlock.lease for cBlock in HDBs]) 
    psmrange   = lrange([cHDB.psm() for cHDB in HDBs]) 

    HDBS = []
    for cHDB in HDBs:
        blockadress = cHDB.blockadress()
        if blockadress in geolocs:
            (HDBgeoloc,reliability) = geolocs[blockadress]
            if HDBgeoloc != None:
                HDB = "{coords: [" + ",".join([str(c) for c in HDBgeoloc]) + "],"
                b = int(255.0 * (1.0 - abscissa(psmrange,float(cHDB.psm()))))
                r = 255 - b
                HDB = HDB + "color: rgbToHex(" + str(r) + ",0," + str(b) + "), lease: " + str(int(cHDB.lease)) + ", psm: " + str(cHDB.psm()) + "}"
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




class HDB:
    def __init__(self,month,town,flat_type,block,street_name,storey_range,floor_area_sqm,flat_model,lease_commence_date,resale_price):
        self.month = month.strip()
        self.town  = town.strip()
        self.flat_type = flat_type.strip()
        self.block = block.strip()
        self.street_name = street_name.strip()
        self.storey_range = storey_range.strip()
        self.floor_area_sqm = float(floor_area_sqm.strip())
        self.flat_model = flat_model.strip()
        self.lease = int(lease_commence_date.strip())
        self.resale_price = float(resale_price.strip())

    def blockadress(self):
        return (self.block + " " + self.street_name).strip()

    def psm(self):
        return int(float(self.resale_price) / float(self.floor_area_sqm))

HDBs = []

for line in content.split("\n")[1:]:
    (month,town,flat_type,block,street_name,storey_range,floor_area_sqm,flat_model,lease_commence_date,resale_price) = line.split(",")
    cHDB = HDB(month,town,flat_type,block,street_name,storey_range,floor_area_sqm,flat_model,lease_commence_date,resale_price)
    HDBs = HDBs + [cHDB]


def blockadress2HDNnumber(HDBs):
    blockadresses = {}
    for cHDB in HDBs:
        blockadress =  cHDB.blockadress()
        if not blockadress in blockadresses:
            blockadresses[blockadress] = 0
        blockadresses[blockadress] += 1


    #sortlist = [(blockadresses[blockadress],blockadress) for blockadress in blockadresses]
    #sortlist.sort()
    #for (n,adress) in sortlist:
    #    puts("adress",adress,"n",n)

    return blockadresses

blockadresses = blockadress2HDNnumber(HDBs)
puts("nblockadresses",len(blockadresses.keys()))

dumpcache(geolocs)
# dumpmappricepersqm(geolocs,HDBs)
dumpmaplease(geolocs,HDBs)

def computegeolocs(HDBs):
    maxnqueries = 0
    nqueries = 0
    nHDB = 0

    for cHDB in HDBs:
        puts("HDB",nHDB,cHDB.blockadress())
        nHDB += 1
        blockadress = cHDB.blockadress()
        if not blockadress in geolocs:
            (coords,reliability) = getgeoloc(cHDB.block,cHDB.street_name)
            puts("adress",blockadress,"coords",coords)
            geolocs[blockadress] = (coords,reliability)
            if not coords == None:
                dumpcache(geolocs)
            nqueries += 1
            if nqueries > maxnqueries:
                break



