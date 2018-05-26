# LSGI3431A System Customization and Development
# Laboratory Exercise 1 - Listing 3.2
#  Demonstration of mutability of List and Tuple
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 27/1/2018


# Define one tuple
coordinate = (826295, 831032)
#Define a site tuple
site = (['Happy School', 'Tsuen Wan'], coordinate)
#Define a list of Building
listOfSite = [site]


#Define a new site (ALLOW NEW OBJECT assigned)

site = (['New Racecourse', 'Sha Tin'], (829091.336, 839194.967))

listOfSite.append(site);
print(listOfSite)

#ERROR: immutable tuple, Try it by toggle comment of next line
site[0] = ['Sha Tin Racecourse', 'Sha Tin']

#OK: Change the mutable object inside a tuple
#COPY BY REFERENCE!!!
(site[0])[0] = 'Sha Tin Racecourse'
print(listOfSite)

for record in listOfSite:
    location, coordinate = record
    name, region = location
    northing, easting = coordinate

    print 'site name: ' + name
