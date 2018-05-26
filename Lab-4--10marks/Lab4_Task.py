"""
  LSGI3431A System Customization and Development
  Laboratory Exercise 3 - Task program
  Trajectory class with storing the Projected Coordinate System (PCS)
  Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
  Date: 2 March 2018
"""

import geopy.distance
import pyproj
import os
import arcpy
import sys


class Traectory:

    def __init__(self, workspace):
        self.__traectory_list = []
        self.traectory_header = ["longitude", "latitude", "altitude", "acquiring date", "acquiring time"]
        self.workspace = workspace + '\\'
        arcpy.env.workspace = self.workspace

    def Read_Points_From_File(self, fileName):
        """
        Read the Geolife Trajectories 1.3 data file
        :param path: The file path for the Trajectories file.
        :return: The extracted trajectories in projected coordinate in Beijing 1954 117E.
        """

        try:
            fp = open(fileName, 'r')

            origSys = pyproj.Proj(init="epsg:4326")
            newSys = pyproj.Proj(init="epsg:2436")

            for line, content in enumerate(fp):
                if line > 5:
                    lineField = content.replace('\n', '').split(',')
                    lat = float(lineField[0])
                    lon = float(lineField[1])
                    #DEBUG ONLY
                    #print 'lat: %f; lon: %f' % (lat, lon)

                    x, y = pyproj.transform(origSys, newSys, lon, lat)
                    # DEBUG ONLY
                    #print 'x: %f; y: %f' % (x, y)
                    alt = float(lineField[3])
                    date = lineField[5]
                    time = lineField[6]
                    temp = (x, y, alt, date, time)
                    self.__traectory_list.append(temp)

            print 'Complete Reading Trajectories.'

            fp.close()
        # Catch the error if the Input/Output related error found
        except IOError:
            print 'The file could not be read!'
            self.__traectory_list = []

    def Points_Counting(self):
        """
        Count how many points are there
        :return: the number of points
        """
        return len(self.__traectory_list)

    def Cal_Dist(self):
        """
        Calculate the Euclidean distance of all points
        :return: The Euclidean distance of all points
        """
        sum_euclidean_dist = 0
        last_point = None
        for index, this_point in enumerate(self.__traectory_list):
            if last_point is not None:
                sum_euclidean_dist = ((last_point[0]-this_point[0])**2+(last_point[0]-this_point[1])**2)**0.5
                # Debug: Show cumulative geodetic distance
                # Checked with the beginning and the last one
                #print sum_geodetic_dist
            last_point = this_point
        return sum_euclidean_dist

    def __str__(self):
        """
        Return all points in this list
        :return: a string with all the points information
        """
        out_str = "\n".join(`"%.5f, %.5f, %.1f, %s, %s" % (point[0], point[1], point[2], point[3], point[4])` for point in self.__traectory_list)
        return "\'x, y, altitude, capture time, capture date'\n"+out_str

    def Point_to_FeatureClass(self, fc):
        """
        Create a ArcGIS Geodatabase feature class with all the points in the list
        :return: null
        """


        feature_class = []
        for index, traectory in enumerate(self.__traectory_list):
            point_row = arcpy.Point(X=traectory[0], Y=traectory[1], Z=traectory[2], ID=index)
            feature_class.append(arcpy.PointGeometry(point_row, arcpy.SpatialReference(2436)))
        arcpy.CopyFeatures_management(feature_class, (self.workspace + '\\' + fc))
        print 'Complete Creating a Point Feature Class'

        return None


    def Add_Attribute(self, fc):
        """
        Modify the ArcGIS Geodatabase feature class's attributes
        :return: null
        """

        updateFields = ['date', 'time']

        for field in updateFields:
            arcpy.AddField_management(fc, field, 'DATE')

        with arcpy.da.UpdateCursor(fc, updateFields) as cursor:
            for i, row in enumerate(cursor):
                for j, field in enumerate(updateFields):
                    row[j] = self.__traectory_list[i][3+j]

                cursor.updateRow(row)


        print 'Complete Reading Attributes'
        return None

    def MBR(self,fc):
        """
        Construct the Minimum Bounding Box of all trajectory points.
        :return: null
        """
        arcpy.MinimumBoundingGeometry_management(fc, self.workspace + "MBB output", "RECTANGLE_BY_AREA")



if __name__ == "__main__":

    """
        Execute as main program...
     """

    """Set default file name and geodatabase name  """
    gdbName = '\\xxx2163xD_Chan.gdb'
    path = os.path.dirname(os.path.abspath(__file__))
    featureClass = 'Trajectory_Points'

    """Check if there are any customized path name and geodatabase name """
    if len(sys.argv) < 3:
        print "Usage: %s <Path of your ArcPy GeoDatabase> <Your Geodatabase name>" % (sys.argv[0])
        print "Example: %s D:/Test/ Default.gdb" % (sys.argv[0])
        print
        print "Now use the default path: %s and name: %s " % (os.path.dirname(os.path.abspath(__file__)), gdbName)
    else:
        path, gdbName = sys.argv[1], sys.argv[2]

    """ Concat the file into full path for checking"""
    workspace = path + gdbName

    """ the file does not exists but write privileges are given """
    """ the normal case we will deal with                       """

    tra = Traectory(workspace)
    tra.Read_Points_From_File('xxx2163xD_Chan.plt')
    num = tra.Points_Counting()
    print 'The number of Points: ', str(num)

    if num != 0:
        distance = tra.Cal_Dist()
        print 'Distance of the whole trajectory: %f meters ' % distance
        # DEBUG
        # For Task 2
        #print 'for task 2: '
        #print str(tra)

    # Task 3
    tra.Point_to_FeatureClass(featureClass)

    # Task 4
    tra.Add_Attribute(featureClass)

    #Task 5
    tra.MBR(featureClass)
    print 'Geodatabase creation successful! You are ready to go!'
    exit(0)

