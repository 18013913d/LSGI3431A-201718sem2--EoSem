from Trajectory import *

# LSGI3431A System Customization and Development
# Laboratory Exercise 3 - Task program
# Test run for Trajectory class
# Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
# Date: 10/2/2018

if __name__ == "__main__":
    tra = Traectory()
    tra.read_points_from_file('xxx2163xD_Chan.plt')
    num = tra.points_counting()
    print 'The number of Points: ' , str(num)
    if num != 0:
        distance = tra.Cal_Dist()
        print 'Distance of the whole trajectory: %f meters ' % distance
        #DEBUG
        #print str(tra)
