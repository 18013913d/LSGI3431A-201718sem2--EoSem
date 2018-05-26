import arcpy
import os

arcpy.CheckOutExtension("Network")

name = {
    "badminton": "Badminton Courts",
    "basketball": "Basketball Courts",
    "country_park": "Country Parks",
    "fitness_center": "Fitness Rooms",
    "others": "Other Recreation & Sports Facilities",
    "parks": "Parks, Zoos and Gardens",
    "grounds": "Sports Grounds",
    "pools": "Swimming Pools"
}

if __name__ == '__main__':

    print "Please input the path for your gdb with all facilities:"
    gdb_name = raw_input(">>> ")

    if gdb_name == "":
        os.write(2, "[ERROR] You haven't type the name of your gdb! Exiting...\n")
        exit(1)

    if not gdb_name.endswith(".gdb"):
        gdb_name += ".gdb"

    if not os.path.isabs(gdb_name):
        cwd = os.getcwd()
        print "[INFO] Convert it to absolute by using the path for the script"
        print "[INFO] i.e. %s" % cwd
        gdb_name = os.path.realpath(os.path.join(cwd, gdb_name))

    arcpy.env.workspace = gdb_name

    print "We assume the walking speed and reasonable walking distance are 5 km/h and 15 minutes respectively."
    speed = 5.00
    reasonable = speed * 15.0 / 60.0 * 1000.0

    print "Please specify a user-defined time to walk in MINUTES: [Default: 5.00]"
    user_time = raw_input(">>> ")

    if user_time == "":
        user_distance = float(speed * 5.00 / 60.0) * 1000.0
    else:
        try:
            user_distance = float(speed * float(user_time) / 60) * 1000.0
            print 'The inputted time: %f' % float(user_time)
        except:
            user_distance = float(speed * 5.00 / 60.0) * 1000.0
    print "The distance for 15 and %f minutes with walking %f km/h are %f and %f meters respectively." % (
    float(user_time), speed, reasonable, user_distance)

    for facility in name.iterkeys():
        # Now all it shall have suitable facility type and distance for walk.
        facilities = arcpy.FeatureSet()
        facilities.load(facility)
        try:
            arcpy.Delete_management("%sWalkingReasonable" % (facility))
        except:
            pass

        try:
            arcpy.Delete_management("%sWalkingUser" % (facility))
        except:
            pass

        # MUST USE OVERLAP to yield correct result. Here, NO_OVERLAP is used for better visuallization.
        arcpy.na.GenerateServiceAreas(facilities, "%f" % (reasonable), "Meters", "Network\\Network_ND",
                                      "%sWalkingReasonable" % (facility), Detailed_Polygons="SIMPLE_POLYS",
                                      Distance_Attribute="Length", Polygon_Trim_Distance=100,
                                      Polygons_for_Multiple_Facilities="NO_OVERLAP",
                                      Polygon_Simplification_Tolerance=25)
        arcpy.na.GenerateServiceAreas(facilities, "%f" % (user_distance), "Meters", "Network\\Network_ND",
                                      "%sWalkingUser" % (facility), Detailed_Polygons="SIMPLE_POLYS"
                                      , Distance_Attribute="Length", Polygon_Trim_Distance=100,
                                      Polygons_for_Multiple_Facilities="NO_OVERLAP",
                                      Polygon_Simplification_Tolerance=25)

        print "%s type finished" % (facility)
