# LSGI3431A System Customization and Development
# Laboratory Exercise 1 - Listing 3.3
# Demonstration of Set and Dictionary
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 27/1/2018


# Define a dictionary
bldgs = {1: "Happy Building", 2: "PolyU", 3:"PolyU"}

#Duplicated key: first value will disposed
bldgs = {1: "Happy Building", 2: "PolyU", 3:"PolyU", 2: "Nam Cheong Station"}

#Output data
for index, bldg in bldgs.iteritems():
    print "ID Number: " + str(index) + ", Value:" + str(bldg)

#Find PolyU
for i in bldgs.iterkeys():
    if bldgs[i] == "PolyU":
        print "PolyU are here: index " + str(i)

    print

#Define a set
newSet = set(["Happy Building", "PolyU", "PolyU"])
if newSet.intersection(set(["PolyU"])):
    print "PolyU in the set!"
