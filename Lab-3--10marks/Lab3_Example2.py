from geopy.distance import great_circle
from geopy.geocoders import GoogleV3

# LSGI3431A System Customization and Development
# Laboratory Exercise 3 - Example 2
# Reproduction of Example 2
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 10/2/2018

geolocator = GoogleV3()
PolyU_name = "Hong Kong Polytechnic University"
PolyU_geocode = geolocator.geocode(PolyU_name)
PolyU_geog_coord = (PolyU_geocode.latitude, PolyU_geocode.longitude)

unb_name = "University of New Brunswick"
unb_geocode = geolocator.geocode(unb_name)
unb_geog_coord = (unb_geocode.latitude, unb_geocode.longitude)

geodetic_dist = great_circle(PolyU_geog_coord, unb_geog_coord).kilometers
print 'The distance between %s and %s are %.3f km' % (PolyU_name, unb_name, geodetic_dist)
