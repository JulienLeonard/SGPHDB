from basics import *

filepaths = ["resale-flat-prices-based-on-registration-date-from-march-2012-onwards.csv","resale-flat-prices-based-on-approval-date-2000-feb-2012.csv"]
hdbs = {}

class HDB:
    def __init__(self,blockadress = "",lease_commence_date=""):
        self.mblockadress = blockadress
        self.mlease_commence_date = lease_commence_date
        self.mntransactions = 0


for filepath in filepaths:
    content = ""
    with open(filepath, 'r') as content_file:
        content = content_file.read()


    

    for line in content.split("\n")[1:]:
        # print line.split(",")
        (month,town,flat_type,block,street_name,storey_range,floor_area_sqm,flat_model,lease_commence_date,resale_price) = line.split(",")
        street_name = street_name.strip()
        block = block.strip()
        blockadress =  (street_name + " " + block).strip()

        if not blockadress in hdbs:
            hdbs[blockadress] = HDB(blockadress,lease_commence_date)
        if not hdbs[blockadress].mlease_commence_date  == lease_commence_date:
            puts("error HDB",blockadress," lease_commence_date 1",hdbs[blockadress].mlease_commence_date,"lease_commence_date 2",lease_commence_date)
        hdbs[blockadress].mntransactions += 1

puts("n hdbs",len(hdbs.keys()))
for adress in sorted(hdbs.keys()):
    puts("adress",adress,"lease_commence_date",hdbs[adress].mlease_commence_date,"ntransactions",hdbs[adress].mntransactions)


