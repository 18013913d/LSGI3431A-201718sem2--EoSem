from geopy.geocoders import GoogleV3

# LSGI3431A System Customization and Development
# Laboratory Exercise 3 - Example 1
# Reproduction of Example 1
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 10/2/2018

geolocator = GoogleV3()
location = "Hong Kong Polytechnic University"
address = geolocator.geocode(location)

print "Location: ", location
print "Address: ", address.address
print "Coordinate: (%f, %f)" % (address.latitude, address.longitude)
