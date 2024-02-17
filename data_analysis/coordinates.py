
from threading import Thread
import pandas as pd
from geopy.geocoders import Nominatim

data = pd.read_csv("src/layoffs.fyi_20240213_201617.csv", sep=';')

# Manual fix wrong city name spelling. If noted print output ex. "Shenzen - None", need to manualy add spelling replacement
data.replace({"Location HQ": "Shenzen"}, "Shenzhen", inplace=True)
data.replace({"Location HQ": "LuxembourgRaleigh"}, "Luxembourg", inplace=True)
data.replace({"Location HQ": "Ferdericton"}, "Fredericton", inplace=True)
data.replace({"Location HQ": "MelbourneVictoria"}, "Melbourne", inplace=True)

geolocator = Nominatim(user_agent="my_geocoder")

threads = 5


def locate_coord( start, end):
    """
    Get latitude, longtitude by City name using geopy
    """

    if "Lat" not in data:
        data["Lat"] = ""
    if "Lon" not in data:
        data["Lon"] = ""

    for i in range(start, end):
        #print(str(i)+" - "+str(data.iloc[i]["Location HQ"]))
        location = geolocator.geocode(data.iloc[i]["Location HQ"], timeout=5)
        if location:
            data.loc[i,"Lat"], data.loc[i,"Lon"] = location.latitude, location.longitude
            print(i)
        else:
            print(str(data.iloc[i]["Location HQ"]) + " - None")
        
        

    #location = geolocator.geocode(row["Location HQ"], timeout=5)
"""
    if location:
        print(row["id"])
        # print(str(row["Location HQ"]) + " " +str(location.latitude)+" "+str(location.longitude))
        return location.latitude, location.longitude
    else:
        print(str(row["Location HQ"]) + " - None")
        return None, None"""


# Clear data
data["Date"] = pd.to_datetime(data["Date"])
data['# Laid Off'] = pd.to_numeric(data['# Laid Off'], errors='coerce')
data.dropna(subset=['# Laid Off'], inplace=True)
data['%'] = pd.to_numeric(data['%'].str.rstrip('%'), errors='coerce')
data.dropna(subset=['%'], inplace=True)
data.drop('id', axis=1, inplace=True)
data.reset_index(drop=True, inplace=True)

rows = len(data.index)

tr:Thread = []
for t in range(threads):
    part = rows//threads
    if t < threads-1:
        tr.append(Thread(target=locate_coord, args=(t*part,t*part+part,)))
        print(str(t*part)+" - "+str(t*part+part))
    else:
        tr.append( Thread(target=locate_coord, args=(t*part,rows)))
        print(str(t*part)+" - "+str(rows))
    
    tr[t].start()
    


for t in tr:
    t.join()
    



#data["Lat"], data["Lon"] = zip(*data.apply(locate_coord, axis=1))

data.to_csv("src/data_coord.csv", encoding='utf-8')

print(data)
