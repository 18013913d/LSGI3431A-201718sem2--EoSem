from geopy.distance import great_circle
from geopy.geocoders import GoogleV3

# LSGI3431A System Customization and Development
# Laboratory Exercise 3 - Example 3
# Reproduction of Example 3
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 10/2/2018

def geodetic_dist(pt1, pt2):
    """
    Calculate and return the geodetic distance between two points
    :param pt1: A tuple containing latitude and longitude of the first point
    :param pt2: A tuple containing latitude and longitude of the second point
    :return: geodetic distance between two points
    """
    if (type(pt1) is not tuple) or (type(pt2) is not tuple):
        print 'Please supply two tuples containing latitude and longitude!'
        return None
    if (len(pt1) != 2 or len(pt2) != 2):
        print 'The point should contain two elements: latitude and longitude only!'
        return None
    if (type(pt1[0]) is not float or type(pt1[1]) is not float or \
        type(pt2[0]) is not float or type(pt2[1]) is not float):
        print 'Please use floating point number to yield meaningful result with reasonable accuracy!'
        return None
    if (pt1[0] < -90.0 or pt1[0] > 90.0 or pt2[0] < -90.0 or pt2[0] > 90.0 ):
        print 'Invalid latitude: it should be between -90.0 to 90.0'
        return None
    if (pt1[1] < -180.0 or pt1[1] > 180.0 or pt2[1] < -180.0 or pt2[1] > 180.0 ):
        print 'Invalid longitude: it should be between -180.0 to 180.0'
        return None

    return great_circle(pt1, pt2).kilometers

if __name__ == "__main__":
    geolocator = GoogleV3()
    PolyU_name = "Hong Kong Polytechnic University"
    PolyU_geocode = geolocator.geocode(PolyU_name)
    PolyU_geog_coord = (PolyU_geocode.latitude, PolyU_geocode.longitude)

    unb_name = "University of New Brunswick"
    unb_geocode = geolocator.geocode(unb_name)
    unb_geog_coord = (unb_geocode.latitude, unb_geocode.longitude)

    dist = geodetic_dist(PolyU_geog_coord, unb_geog_coord)
    if dist is not None:
        print 'The distance between %s and %s are %.3f km' % (PolyU_name, unb_name, dist)
