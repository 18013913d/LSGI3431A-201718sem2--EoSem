"""
 LSGI3431A System Customization and Development
 Laboratory Exercise 4 - Task 1 Program
 Create a file geodatabase with customized file path
 Created By Chan Tsz Kin, Jimmy (LSGI), Student Number: xxx2163xD
 Date: 2 March 2018

"""

import arcpy
import sys
import os

def Generate_GDB(path, gdbName):
    """
    Using ArcPy environment to generate a geodatabase
    :param path: The path of the geodatabase
    :param gdbName: The name of the geodatabase
    :return: null
    """
    arcpy.env.workspace = path
    arcpy.CreateFileGDB_management(path, gdbName)
    return None

if __name__ == "__main__":
    """
       Execute as main program...
    """

    """Set default file name and geodatabase name  """
    gdbName = '\\xxx2163xD_Chan.gdb'
    path = os.path.dirname(os.path.abspath(__file__))

    """Check if there are any customized path name and geodatabase name """
    if len(sys.argv) < 3:
        print "Usage: %s <Path of your ArcPy GeoDatabase> <Your Geodatabase name>" % (sys.argv[0])
        print "Example: %s D:/Test/ Default.gdb" % (sys.argv[0])
        print
        print "Now use the default path: %s and name: %s " % (os.path.dirname(os.path.abspath(__file__)), gdbName)
    else:
        path, gdbName = sys.argv[1], sys.argv[2]
    """ Concat the file into full path for checking"""
    fullFilePath = path + gdbName

    if os.path.exists(fullFilePath):
        """ the file is there """
        print "[ERROR] The geodatabase of path %s are probably exists... Please copy or move your geodatabase..." % fullFilePath
        exit(1)
    elif os.access(os.path.dirname(fullFilePath), os.W_OK):
        """ the file does not exists but write privileges are given """
        """ the normal case we will deal with                       """
        Generate_GDB(path, gdbName)
        print 'Geodatabase creation successful! You are ready to go!'
        exit(0)
    else:
        """ can not write there """
        print "You have no privilage to write in this folder: %s" % path
        exit(1)
