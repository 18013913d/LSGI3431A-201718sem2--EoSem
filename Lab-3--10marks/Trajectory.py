from geopy.distance import great_circle

# LSGI3431A System Customization and Development
# Laboratory Exercise 3 - Trajectory class
# The class of trajectory
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 10/2/2018

class Traectory:

    def __init__(self):
        self.__traectory_list = []
        self.traectory_header = ["longitude", "latitude", "altitude", "acquiring date", "acquiring time"]

    def read_points_from_file(self, fileName):
        """
        Read the Geolife Trajectories 1.3 data file
        :param path: The file path for the Trajectories file.
        :return: The extracted trajectories.
        """
        try:
            fp = open(fileName, 'r')

            for line, content in enumerate(fp):
                if line > 5:
                    lineField = content.replace('\n', '').split(',')
                    lat = float(lineField[0])
                    lon = float(lineField[1])
                    alt = float(lineField[3])
                    date = lineField[5]
                    time = lineField[6]
                    temp = (lat, lon, alt, date, time)
                    self.__traectory_list.append(temp)

            print 'Complete Reading Trajectories.'

            fp.close()
        # Catch the error if the Input/Output related error found
        except IOError:
            print 'The file could not be read!'
            self.__traectory_list = []

    def points_counting(self):
        return len(self.__traectory_list)

    def Cal_Dist(self):
        sum_geodetic_dist = 0
        last_point = None
        for index, this_point in enumerate(self.__traectory_list):
            if last_point is not None:
                # Reminder: THE POINT STORE THE LATITUDE IN 0 AND LONGITUDE IN 1!!!!
                sum_geodetic_dist += great_circle((last_point[0], last_point[1]),(this_point[0],this_point[1])).meters
                # Debug: Show cumulative geodetic distance
                # Checked with the beginning and the last one
                #print sum_geodetic_dist
            last_point = this_point
        return sum_geodetic_dist

    def __str__(self):
        out_str = "\n".join(`"%.5f, %.5f, %.1f, %s, %s" % (point[1], point[0], point[2], point[3], point[4])` for point in self.__traectory_list)
        return "\'longitude, latitude, altitude, capture time, capture date'\n"+out_str

