import sys
import os
import csv



class Facility:
    def __init__(self, category, name, header, tuples):
        self._category = category
        self._name = name[category]
        self._workspace = None
        del header[0]
        self._fieldName = {"Name"    : header.index("ENGLISH NAME"),
                         "Address"  : header.index("ENGLISH ADDRESS"),
                         "Longitude": header.index("LONGITUDE"),
                         "Latitude" : header.index("LATITUDE"),
                         "Easting"  : header.index("EASTING"),
                         "Northing" : header.index("NORTHING"),
                         "District" : None,
                         "Type"     : None}
        if "DISTRICT" in header:
            self._fieldName["District"] = header.index("DISTRICT")
        else:
            self._fieldName.pop("District")
        if "FACILITY TYPE" in header:
            self._fieldName["Type"] = header.index("FACILITY TYPE")
        else:
            self._fieldName.pop("Type")

        self._facilities = [[field for (j, field) in enumerate(tuple) if j != 0] for (i, tuple) in enumerate(tuples)]

    def __str__(self):
        return "\n".join(str(tuple) for tuple in self._facilities)

    def __iter__(self):
        return iter(self._facilities)

    def __len__(self):
        return len(self._facilities)

    def category(self):
        return self._category

    def get_header(self):
        header = ["CATEGORY", "ENGLISH NAME", "ENGLISH ADDRESS", "LONGITUDE", "LATITUDE", "EASTING", "NORTHING", "DISTRICT", "FACILITY TYPE"]
        if "DISTRICT" not in self._fieldName:
            header.remove("DISTRICT")
        if "FACILITY TYPE" not in self._fieldName:
            header.remove("FACILITY TYPE")
        return header

    @property
    def tuples(self):
        return self._facilities

    @tuples.setter
    def tuples(self, column, index):
        self._facilities.insert(index, column)

    @tuples.setter
    def tuples(self, column):
        self._facilities.append(column)

    def pop(self, index):
        try:
            return self._facilities.pop(index)
        except IndexError:
            os.write(2, "[ERROR] No index %d in the class %s found\n" % (index, self._name))
            return None

    def has_distrct(self):
        if self._fieldName["District"] is None:
            return False
        else:
            return True

    def has_type(self):
        if self._fieldName["Type"] is None:
            return False
        else:
            return True

    def to_feature_class(self, gdb_path, gdb_name):
        import arcpy
        abspath = gdb_path

        if (os.path.isabs(abspath) == False):
            print "[INFO] The path %s for ESRI Geodatabase is not absolute." % (gdb_path)
            print "[INFO] Automatically changed to absolute by using the file path of this script."
            abspath = os.path.join(os.getcwd(), abspath)
            print "[INFO] New path: %s" % (abspath)

        if not os.path.isdir(os.path.join(abspath, gdb_name)):
            arcpy.CreateFileGDB_management(abspath, gdb_name)
        self._workspace = os.path.join(abspath, gdb_name)
        arcpy.env.workspace = self._workspace

        print "[INFO] Now handle the file type of %s" % (self._name)

        points = []
        for (i, tuple) in enumerate(iter(self)):
            #print str(tuple)
            point = arcpy.Point(X=float(tuple[self._fieldName["Easting"]]), Y=tuple[self._fieldName["Northing"]], ID=i+1)
            points.append(arcpy.PointGeometry(point, arcpy.SpatialReference(2326)))
        arcpy.CopyFeatures_management(points, os.path.join(self._workspace,self._category))

        field_to_update = [k for k in self._fieldName.iterkeys()]

        arcpy.AddField_management(in_table=self._category, field_name="Name", field_type="TEXT")
        arcpy.AddField_management(in_table=self._category, field_name="Address", field_type="TEXT")
        arcpy.AddField_management(in_table=self._category, field_name="Longitude", field_type="DOUBLE")
        arcpy.AddField_management(in_table=self._category, field_name="Latitude", field_type="DOUBLE")
        arcpy.AddField_management(in_table=self._category, field_name="Easting", field_type="DOUBLE")
        arcpy.AddField_management(in_table=self._category, field_name="Northing", field_type="DOUBLE")
        if self._fieldName.has_key("District"):
            arcpy.AddField_management(in_table=self._category, field_name="District", field_type="TEXT")
        if self._fieldName.has_key("Type"):
            arcpy.AddField_management(in_table=self._category, field_name="Type", field_type="TEXT")

        with arcpy.da.UpdateCursor(in_table=self._category, field_names=field_to_update) as cursor:
            for (i, row) in enumerate(cursor):
                for (j, field) in enumerate(field_to_update):
                    row[j] = self._facilities[i][self._fieldName[field]]
                cursor.updateRow(row)

    def find_nearest(self, latitude, longitude):

        import geopy.distance as geodesic

        search = (latitude, longitude)
        shortest = float('inf')
        shortest_name = None
        for i, tuple in enumerate(iter(self)):
            this_point = (tuple[self._fieldName["Latitude"]], tuple[self._fieldName["Longitude"]])
            dist = geodesic.great_circle(search, this_point).meters
            if abs(dist - shortest) > 0.001 and dist < shortest:
                shortest = dist
                shortest_name = [self._facilities[i][self._fieldName["Name"]]]
            elif abs(dist - shortest) < 0.001:
                shortest_name.append(self._facilities[i][self._fieldName["Name"]])

        return shortest, shortest_name

    @staticmethod
    def find_nearest_geodatabase(gdb_path, gdb_name, latitude, longitude, all_facilities):
        import arcpy
        import geopy.distance as geodesic
        abspath = gdb_path

        if (os.path.isabs(abspath) == False):
            print "[INFO] The path %s for ESRI Geodatabase is not absolute." % (gdb_path)
            print "[INFO] Automatically changed to absolute by using the file path of this script."
            abspath = os.path.join(os.getcwd(), abspath)
            print "[INFO] New path: %s" % (abspath)
        workspace = os.path.join(abspath, gdb_name)
        arcpy.env.workspace = workspace
        shortest = float('inf')
        search = (latitude, longitude)
        name = None
        try:
            arcpy.Delete_management("shortest_one")
        except:
            pass

        for facility in all_facilities.iterkeys():
            try:
                with arcpy.da.SearchCursor(os.path.join(workspace, facility), ["Latitude", "Longitude", "Name"]) as cursor:
                    arcpy.MakeFeatureLayer_management(facility, "temp_layer")
                    for row in cursor:
                        this_fac = (row[0], row[1])
                        dist = geodesic.great_circle(search, this_fac).meters
                        if abs(dist - shortest) > 0.001 and dist < shortest:
                            shortest = dist
                            name = [row[2]]
                            arcpy.SelectLayerByAttribute_management("temp_layer", "NEW_SELECTION",
                                                                    "\"Name\"='"+row[2]+"'")
                        elif abs(dist - shortest) < 0.001:
                            if row[2] not in name:
                                name.append(row[2])
                            arcpy.SelectLayerByAttribute_management("temp_layer", "ADD_TO_SELECTION",
                                                                    "\"Name\"='" + row[2] + "'")

            except:
                os.write(2, "[ERROR] The geodatabase %s have no %s feature class. Skipping.\n" % (os.path.join(workspace, facility), facility))
                continue
            else:
                arcpy.Delete_management("shortest_one")
                arcpy.CopyFeatures_management("temp_layer", "shortest_one")
            finally:
                arcpy.Delete_management("temp_layer")
        if shortest == float('inf') or name is None:
            raise ValueError
        return shortest, name

    @staticmethod
    def gdb_to_class(key, gdb_path, gdb_name, name):

        import arcpy

        workspace = os.path.join(gdb_path, gdb_name)
        arcpy.env.workspace = workspace

        tuples = []
        header = ["CATEGORY", "ENGLISH NAME", "ENGLISH ADDRESS", "LONGITUDE", "LATITUDE", "EASTING", "NORTHING", "DISTRICT", "FACILITY TYPE"]
        try:
            with arcpy.da.SearchCursor(os.path.join(workspace, key), "*") as cursor:
                if "District" not in cursor.fields:
                    header.remove("DISTRICT")
                if "Type" not in cursor.fields:
                    header.remove("FACILITY TYPE")
                index = []
                index.append(cursor.fields.index("Name"))
                index.append(cursor.fields.index("Address"))
                index.append(cursor.fields.index("Longitude"))
                index.append(cursor.fields.index("Latitude"))
                index.append(cursor.fields.index("Easting"))
                index.append(cursor.fields.index("Northing"))

                if "DISTRICT" in header:
                    index.append(cursor.fields.index("District"))
                if "FACILITY TYPE" in header:
                    index.append(cursor.fields.index("Type"))

                for row in cursor:
                    tuple = [name[key]]
                    tuple.append(row[index[0]])
                    tuple.append(row[index[1]])
                    tuple.append(row[index[2]])
                    tuple.append(row[index[3]])
                    tuple.append(row[index[4]])
                    tuple.append(row[index[5]])
                    if "DISTRICT" in header:
                        tuple.append(row[index[6]])
                    if "FACILITY TYPE" in header:
                        tuple.append(row[index[7]])
                    tuples.append(tuple)
        except:
            os.write(2, "[ERROR] The facility %s occured error while reading.\n" % (k))

        return Facility(key, name, header, tuples)





def input_path(all, type):
    '''
    Let the user input a path without checking.
    :param all: a dictionary housing key to name mapping. (e.g. pools --> "swimming pools"
    :param type: the current type of facility.
    :return: the inputted file path
    '''
    print "Please input the absolute csv file path for the type %s. Type nothing to skip." % (all[type])
    filepath = raw_input(">>> ")
    return filepath



def validate_path(all, **kwargs):
    '''
    Validate a facility file path and open a file descriptor to the file.
    :param all:    a dictionary housing key to name mapping. (e.g. pools --> "swimming pools"
    :param kwargs: a named argument with two info:
                   type: the current type of the facility
                   path: the inputted file path of the current facility
    :return:       a file descriptors pointing towards the current file.
    '''

    # Relative path handling: Assume the relative path are relative to the python script
    pwd = os.getcwd()
    abspath = kwargs["path"]
    fp = None

    # Check if the inputted path is relative. If it is relative, change it to absoulte
    if (os.path.isabs(kwargs["path"]) == False):
        print "[INFO] Automatically changed to absolute by using the file path of this script."
        abspath = os.path.join(pwd, kwargs["path"])
        print "[INFO] New path: %s" % (abspath)

    # Try to give read file descriptors of the file with the absolute path
    if kwargs["operation"] == "r":
        try:
            fp = open(abspath, "r")
        except:
            os.write(2,"[ERROR] File %s for type %s could not be accessed.\n" % (abspath, all[kwargs["type"]]))
            raise IOError
    elif kwargs["operation"] == "w":
        try:
            fp = open(abspath, "w")
        except:
            os.write(2, "[ERROR] File %s for type %s could not be written.\n" % (abspath, all[kwargs["type"]]))
            raise IOError
        else:
            fp.close()
            return abspath
    else:
        fp = abspath
    # Return the file descriptors to the main program
    return fp




flag = False

name = {"badminton" : "Badminton Courts",
        "basketball" : "Basketball Courts",
        "country_park" : "Country Parks",
        "fitness_center" : "Fitness Rooms",
        "others" : "Other Recreation & Sports Facilities",
        "parks" : "Parks, Zoos and Gardens",
        "grounds" : "Sports Grounds",
        "pools" : "Swimming Pools"}


fp = {k:None for k in name.iterkeys()}
facilities = {k:None for k in name.iterkeys()}


# Handle the execution flow if it is running as main program
if (__name__ == "__main__"):

    # print the program header if it is running as main program.
    print "-----------------------------------------------------------"
    print "---        2017/18 Semester 2 - LSGI3431A Project       ---"
    print "---  Theme: Sport and outdoor facilities in Hong Kong   ---"
    print "---    Individual Work: Data conversion for facilities  ---"
    print "---      Module created by CHAN Tsz-kin, 17021636D      ---"
    print "---   Department of Land Surveying and Geoinformatics   ---"
    print "---           Hong Kong Polytechnic University          ---"
    print "-----------------------------------------------------------"

    print

    # First check if arguments are provided already

    if (len(sys.argv) == 1):
        # No argument provided
        while input != "0":
            print "Please input the number of your interested action..."
            print "1 - Read facilities csv files."
            print "2 - Export read data to ESRI Geodatabase."
            print "3 - Find the nearest facilities (with Geodatabase)."
            print "4 - Find the nearest facilities (without Geodatabase)."
            print "5 - Export ESRI Geodatabase into csv"
            print "0 - Exit"
            input = raw_input(">>> ")

            if input == "1":
                print "Please input the facilities path one by one..."

                # Get the file descriptors one by one
                for k in fp.iterkeys():
                    try:
                        input = input_path(name, k)
                        if input != "":
                            fp[k] = validate_path(name, type=k, path=input, operation="r")
                    except IOError:
                        os.write(2, "[ERROR] Could not read a file from facility %s. Continue to next facility.\n" % (name[k]))

                # Now read the file if the file descriptors exists
                for (k, v) in fp.iteritems():
                    # Skip if the file is not valid
                    if v is None:
                        continue
                    reader = csv.reader(v, delimiter=",", quotechar="\"")
                    all_data = [line for line in reader]
                    header = all_data.pop(0)
                    facilities[k] = Facility(k, name, header, all_data)
                    v.close()



            if input == "2":
                print "Please input your gdb path. Type nothing to use current directory: %s" % (os.getcwd())
                path = raw_input(">>> ")
                path = validate_path(path=path, operation="v", all=None)

                print "Please input your gdb name."
                filename = raw_input(">>> ")
                if not filename.endswith(".gdb"):
                    filename += ".gdb"
                for (k, v) in facilities.iteritems():
                    if v is not None:
                        v.to_feature_class(path, filename)

            if input == "3":
                print "Please input your gdb path. Type nothing to use current directory: %s" % (os.getcwd())
                path = raw_input(">>> ")
                path = validate_path(path=path, operation="f", all=None)

                print "Please input your gdb name."
                filename = raw_input(">>> ")
                if not filename.endswith(".gdb"):
                    filename += ".gdb"

                latitude = raw_input("Please input your current latitude: ")
                longitude = raw_input("Please input your current longitude: ")

                if len(latitude.split("-")) == 3:
                    #Degree-Minute-Second
                    temp = latitude.split("-")
                    latitude = float(temp[0]) * 60 * 60 + float(temp[1]) * 60 + float(temp[2])
                try:
                    latitude = float(latitude)
                    if latitude > 90.0 or latitude < -90.0:
                        raise ValueError
                except TypeError:
                    os.write(2, "[ERROR] The input format are wrong. Please input in [DEG-MIN-SEC] OR [DEG.DECIMAL]\n")
                    continue
                except ValueError:
                    os.write(2, "[ERROR] The inputted number are out of range: %f" % (latitude))
                    continue


                if len(longitude.split("-")) == 3:
                    #Degree-Minute-Second
                    temp = longitude.split("-")
                    longitude = float(temp[0]) * 60 * 60 + float(temp[1]) * 60 + float(temp[2])
                try:
                    longitude = float(longitude)
                    if longitude > 180.0 or longitude < -180.0:
                        raise ValueError
                except TypeError:
                    os.write(2, "[ERROR] The input format are wrong. Please input in [DEG-MIN-SEC] OR [DEG.DECIMAL]\n")
                    continue
                except ValueError:
                    os.write(2, "[ERROR] The inputted number are out of range: %f" % (longitude))

                shortest, shortestName = float('inf'), None

                try:
                    shortest, shortestName = Facility.find_nearest_geodatabase(path, filename, latitude, longitude, name)
                except ValueError:
                    os.write(2, "[ERROR] No available facilities found.\n")
                    continue
                print "The nearest facility to (%f, %f) are %s, distance are %f" % (latitude, longitude, ", ".join(facility for facility in shortestName), shortest)

            if input == "4":
                noneCount = 0
                for v in facilities.itervalues():
                    if v is None:
                        noneCount += 1
                if noneCount == len(facilities):
                    os.write(2, "[ERROR] You need to read the data before you can use this function!\n")
                    continue
                latitude = raw_input("Please input your current latitude: ")
                longitude = raw_input("Please input your current longitude: ")

                if len(latitude.split("-")) == 3:
                    # Degree-Minute-Second
                    temp = latitude.split("-")
                    latitude = float(temp[0]) * 60 * 60 + float(temp[1]) * 60 + float(temp[2])
                try:
                    latitude = float(latitude)
                    if latitude > 90.0 or latitude < -90.0:
                        raise ValueError
                except TypeError:
                    os.write(2,
                             "[ERROR] The input format are wrong. Please input in [DEG-MIN-SEC] OR [DEG.DECIMAL]\n")
                    continue
                except ValueError:
                    os.write(2, "[ERROR] The inputted number are out of range: %f" % (latitude))
                    continue

                if len(longitude.split("-")) == 3:
                    # Degree-Minute-Second
                    temp = longitude.split("-")
                    longitude = float(temp[0]) * 60 * 60 + float(temp[1]) * 60 + float(temp[2])
                try:
                    longitude = float(longitude)
                    if longitude > 180.0 or longitude < -180.0:
                        raise ValueError
                except TypeError:
                    os.write(2,
                             "[ERROR] The input format are wrong. Please input in [DEG-MIN-SEC] OR [DEG.DECIMAL]\n")
                    continue
                except ValueError:
                    os.write(2, "[ERROR] The inputted number are out of range: %f" % (longitude))

                shortest, shortest_name = float('inf'), None

                try:
                    for v in facilities.itervalues():
                        if v is None:
                            continue
                        this_shortest, this_shortest_name = v.find_nearest(latitude, longitude)
                        if abs(this_shortest - shortest) > 0.001 and this_shortest < shortest:
                            shortest = this_shortest
                            shortest_name = this_shortest_name
                        elif abs(this_shortest - shortest) < 0.001:
                            for facility in this_shortest_name:
                                if facility not in shortest_name:
                                    shortest_name += this_shortest_name
                except ValueError:
                    os.write(2, "[ERROR] No available facilities found.\n")
                    continue
                print "The nearest facility to (%f, %f) are %s, distance are %f" % (
                    latitude, longitude, ", ".join(facility for facility in shortest_name), shortest)

            if input == "5":

                for k in fp.iterkeys():
                    facilities[k] = None
                    try:
                        input = input_path(name, k)
                        if input != "":
                            fp[k] = validate_path(name, type=k, path=input, operation="w")
                    except IOError:
                        os.write(2, "[ERROR] Could not read a file from facility %s. Continue to next facility.\n" % (name[k]))
                print "Please input your gdb path. Type nothing to use current directory: %s" % (os.getcwd())
                path = raw_input(">>> ")
                path = validate_path(path=path, operation="v", all=None)

                print "Please input your gdb name."
                filename = raw_input(">>> ")

                if not filename.endswith(".gdb"):
                    filename += ".gdb"

                for (k, v) in fp.iteritems():
                    if v is None:
                        continue
                    facilities[k] = Facility.gdb_to_class(k, path, filename, name)
                    with open(v, 'w') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')

                        writer.writerow([column.encode('utf-8') if not isinstance(column, float) else str(column)
                                         for column in facilities[k].get_header()])
                        for facility in iter(facilities[k]):
                            writer.writerow([name[k]]+[column.encode('utf-8') if not isinstance(column, float) else str(column)
                                         for column in facility])

            if input == "0":
                break

            print