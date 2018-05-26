### LSGI3431A System Customization and Development
### Laboratory Exercise 2 - Task 3 Program
### Geolife Trajectories 1.3 Reader
### Date: 5/2/2018
### By CHAN Tsz-kin, Jimmy, xxx2163xD
### Dept. of Land Surveying and Geoinformatics (LSGI), PolyU, Hong Kong


import sys

def Read_Points_from_File(fileName):
    """
    Read the Geolife Trajectories 1.3 data file
    :param path: The file path for the Trajectories file.
    :return: The extracted trajectories.
    """
    point_list = []
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
                point_list.append(temp)

        print 'Data reading done.'

        fp.close()
    # Catch the error if the Input/Output related error found
    except IOError:
        print 'The file could not be read!'
        point_list = None
    finally:
        return point_list

if __name__ == '__main__':
    filePath = '.\\data\\xxx2163xD_Chan.plt'
    print 'GeoLife Trajectories 1.3 Reader By CHAN Tsz-kin, Jimmy.'
    print
    if len(sys.argv) != 2:
        print 'Normal Usage: python Lab2_Task3.py <your trajectory file full path>'
        print 'e.g. python '+ sys.argv[0] +' .\\data\\12345678D_Chan.plt'
        print 'Now use the default one, i.e. .\\data\\xxx2163xD_Chan.plt'
        print
    else:
        filePath = sys.argv[1]

    points_list = Read_Points_from_File(filePath)
    print len(points_list)
