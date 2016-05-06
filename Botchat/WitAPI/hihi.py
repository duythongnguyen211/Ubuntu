import re,requests
a = requests.get('http://www.geoiptool.com/')
raw = a.text
latlon = re.search('GPoint(([^)]+))',raw).groups(0)
lat,lon = map(float,latlon[0].split(","))
print "Latitude:%s   Longitude:%s"%(lat,lon)