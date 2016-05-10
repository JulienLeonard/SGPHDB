from geolocutils import *
from basics import *
# define geolocs
from geoloccache import *

#
# correspond to a HDB block
# ID = blockadress
#
class HDB:
    def __init__(self,town,block,street_name,lease_commence_date):
        self.town  = town.strip()
        self.block = block.strip()
        self.street_name = street_name.strip()
        self.lease = int(lease_commence_date.strip())
        self.sales = []
        
    def blockadress(self):
        return (self.block + " " + self.street_name).strip()

    def addsale(self,sale):
        self.sales.append(sale)

#
# correspond to a sale in a HDB block
#
class Sale:
    def __init__(self,HDB,month,flat_type,storey_range,floor_area_sqm,flat_model,resale_price):
        self.HDB = HDB
        self.month = month.strip()
        self.flat_type = flat_type.strip()
        self.storey_range = storey_range.strip()
        self.floor_area_sqm = float(floor_area_sqm.strip())
        self.flat_model = flat_model.strip()
        self.resale_price = float(resale_price.strip())

    def psm(self):
        return int(float(self.resale_price) / float(self.floor_area_sqm))

#
# create the map of HDB according to lease start time
#
def dumpmaplease(geolocs,HDBs):

    with open("viewtemplate.html", 'r') as content_file:
        template = content_file.read()

    leases     = {cHDB: HDBs[cHDB].lease for cHDB in HDBs}
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

#
# create the map of HDB according to their sqm
#
def dumpmapsqm(geolocs,HDBs):

    with open("viewtemplate.html", 'r') as content_file:
        template = content_file.read()

    sqms     = {cHDB: [] for cHDB in HDBs}
    for cHDB in HDBs:
        sqms[cHDB] = sqms[cHDB] +[HDBs[cHDB].floor_area_sqm]
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

#
# create the map of HDB according to their ppsqm
#
def dumpmappricepersqm(geolocs,HDBs):

    with open("viewtemplate.html", 'r') as content_file:
        template = content_file.read()

    leaserange = lrange([cBlock.lease for cBlock in HDBs.values()]) 
    psmrange   = lrange([cHDB.psm() for cHDB in HDBs.values()]) 

    HDBS = []
    for cHDB in HDBs,values():
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

#
# create cache geoloc
#
def dumpcache(geolocs):
    scache = []
    for key in geolocs:
        if geolocs[key] != None:
            scache.append( "\"" + key.strip() + "\":" "[" + ",".join([str(c) for c in geolocs[key]]) + "]")

    file = open("geoloccache.py", "w")
    file.write("geolocs = {" + ",\n".join(scache) + "}")
    file.close()

#
# check all geolocs of HDBs
#
def computegeolocs(HDBs):
    maxnqueries = 1000
    nqueries = 0
    nHDB = 0

    for cHDB in HDBs.values():
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


def main():
    filepaths = ["resale-flat-prices-based-on-registration-date-from-march-2012-onwards.csv","resale-flat-prices-based-on-approval-date-2000-feb-2012.csv"]
    HDBs = {}
    
    for filepath in filepaths:
        content = ""
        with open(filepath, 'r') as content_file:
            content = content_file.read()

        for line in content.split("\n")[1:]:
            (month,town,flat_type,block,street_name,storey_range,floor_area_sqm,flat_model,lease_commence_date,resale_price) = line.split(",")
            street_name = street_name.strip()
            block       = block.strip()
            blockadress =  block + " " + street_name

            if not blockadress in HDBs:
                cHDB = HDB(town,block,street_name,lease_commence_date)
                HDBs[blockadress] = cHDB
            HDBs[blockadress].addsale(Sale(blockadress,month,flat_type,storey_range,floor_area_sqm,flat_model,resale_price))

    computegeolocs(HDBs)
    dumpcache(geolocs)
    dumpmaplease(geolocs,HDBs)

main()
