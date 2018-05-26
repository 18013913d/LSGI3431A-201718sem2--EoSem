import arcpy
from arcpy.sa import *
from arcpy import env

# Check out the ArcGIS Spatial Analyst extension license and set the workspace, cell size and extent.(almost 4 lines)

# Check out spatial analysis extension


# First Check whether Spatial analysis extension are available.
if arcpy.CheckOutExtension("Spatial") == "Available":
    arcpy.CheckOutExtension("Spatial")

# Workspace setting up
env.workspace = ".\\Sch_location.gdb"
env.cellSize = ".\\Sch_location.gdb\\elevation"
env.extent = ".\\Sch_location.gdb\\elevation"

# Debug: print if environment import are correct...
#print "ArcPy setup finished"








def Distance_Slope(Input_File, Slope_Dist_Output):
    '''
    This Function is for : (1) deriving the slope of the research area
    and (2) figuring out the Euclidean distance from each pixel to its nearest school and recreational site.
    :param Input_File: The dictionary with key as data type, and the value as the associated file name.
    :param Slope_Dist_Output: The dictionary with key as (output) data type, and the value as the associated file name.
    '''

    # Derive the slope from elevation, and save it in geodatabase.(almost 2 lines)

    # First update the slope dictionary of layer's name
    # Then calculate the slope
    Slope(Input_File["DEM"], "DEGREE", 0.3048).save(Slope_Dist_Output["slope"])

    print "Slope Derived"


    # Derive the Euclidean distance to schools, and save it in geodatabase.(almost 2 lines)
    EucDistance(Input_File["schools"]).save(Slope_Dist_Output["schools"])

    print "School_Distance Derived"
    # Derive the Euclidean distance to recreational sites, and save it in geodatabase.(almost 2 lines)
    EucDistance(Input_File["rec_sites"]).save(Slope_Dist_Output["rec_sites"])


    print "Recreation_Distance Derived"


def Reclassification(Slope_Dist_Output, Reclass_Dict, Reclass_Level):
    '''
    This function is for slicing and reclassifying the derived datasets (e.g., slope, distance to school).
    :param Slope_Dist_Output: The dictionary with key as data type, and the value as the associated file name.
    :param Reclass_Dict: The dictionary with key as (output) data type, and the value as the associated file name.
    :param Reclass_Level: A number describing how many levels are used to distinguish the suitability of each pixel
    '''

    # Use a for loop to finish a reversed remap value which applies higher new values to the values
    # representing the suitable place.(almost 2 lines)


    reverse_table = []

    # Define the reverse table
    # Reverse table shall be [ [oldVal, newVal], [oldVal2, newVal2] ...]

    # The mapping of reclass [1, n-0], [2, n-1], [3, n-2]...[n,n-n+1]
    for i in range(0,Reclass_Level):
        reverse_table.append([i+1,Reclass_Level-i])





    # Slice the slope and reverse the values apply higher new values which are representing less steep slope
    # by reclassifying. Then save the reclassified result in geodatabase.(almost 3 lines)
    outSlice_slope = Slice(Slope_Dist_Output["slope"], Reclass_Level, "EQUAL_INTERVAL")
    outreclass_slope = Reclassify(outSlice_slope, "Value", RemapValue(reverse_table))
    outreclass_slope.save(Reclass_Dict["slope"])

    print "Slope_Reclassified"

    # Slice the distance to recreational sites and reverse the values apply higher new values which are representing
    # nearer distance to recreation site by reclassifying. Then save the reclassified result in geodatabase.(almost 3 lines)
    outSlice_rec = Slice(Slope_Dist_Output["rec_sites"], Reclass_Level, "EQUAL_INTERVAL")
    outreclass_rec = Reclassify(outSlice_rec, "Value", RemapValue(reverse_table))
    outreclass_rec.save(Reclass_Dict["rec_sites"])

    print "Recreation_Distance_Reclassified"

    # Slice the distance to schools. Then save the sliced result in geodatabase.(almost 2 lines)
    Slice(Slope_Dist_Output["schools"], Reclass_Level, "EQUAL_INTERVAL").save(Reclass_Dict["schools"])

    print "School_Distance_Reclassified"


def Weighted_Overlay(Input_File, Reclass_Dict, Influence, Slp_remapvalue, Sch_remapvalue, Rec_remapvalue, Landuse_remapvalue):
    '''
    This function is for weighted overlaying and combining reclassified datasets.
    :param Input_File: The dictionary with key as data type, and the value as the associated file name.
    :param Reclass_Dict: The dictionary with key as data type, and the value as the associated file name.
    :param Influence: The Influence Value for each dataset in Weighted Overlay.
    :param Slp_remapvalue,Sch_remapvalue,Landuse_remapvalue: The remap value of corresponding datasets.
    '''

    # Derive the suitable remap value for different datasets, using function: Scaled_Value. (almost 3 lines)
    # Make use of remap value function
    # Notice the value are already reversed.
    slope_remapvalue = Scaled_Value(len(Slp_remapvalue), Slp_remapvalue)
    dis_sch_remapvalue = Scaled_Value(len(Sch_remapvalue), Sch_remapvalue)
    dis_rec_remapvalue = Scaled_Value(len(Rec_remapvalue), Rec_remapvalue)



    # Combine the slope, the distance to schools, the distance to recreational sites and land use map using function weighted overlay.
    # And save the result of weighted overlay in geodatabase.(at least 12 lines)

    # DIFFICULT PART: USING LIST COMPREHENSION TO CREATE NEW LIST
    # The concept: for each item of Landuse_remapvalue, get the key k and value v and put them in the format of [k,v] sublist
    landuse_remap_list = [[k, v] for (k, v) in Landuse_remapvalue.iteritems()]


    # Create WOTable by declaring each feature class, the value to be weighted and their remap value.
    outSuit = WOTable([[Reclass_Dict["slope"], Influence["slope"], "VALUE", RemapValue(slope_remapvalue)],
                       [Reclass_Dict["schools"], Influence["schools"], "VALUE", RemapValue(dis_sch_remapvalue)],
                       [Reclass_Dict["rec_sites"], Influence["rec_sites"], "VALUE", RemapValue(dis_rec_remapvalue)],
                       [Input_File["landuse"], Influence["landuse"], "LANDUSE", RemapValue(landuse_remap_list)]
                       ],
                       [1,10,1]) ### Hard code the 10 result
    outWeightedOverlay = WeightedOverlay(outSuit)
    outWeightedOverlay.save("weighted_out") #Save it as raster layer





    print "Weighted Overlay Completed"


def Filter_FinalSite(Final_Site, Input_File):
    '''
    This function is for recommending the optimal candidate locations based on some more certeria.
    :param Final_Site: The name of output polygon feature class showing the optimal candidate locations.
    :param Input_File: The dictionary with key as data type(input file), and the value as the associated file name.
    :return:
    '''
    # Find the maximum pixel value within the research area, and make a conditional evaluation on each of the input cells.
    # Then save the result of conditional evaluation in geodatabase.(almost 3 lines)

    # Get the highest value we could found
    Value_Max = arcpy.GetRasterProperties_management("weighted_out", "MAXIMUM")
    outCon = Con("weighted_out", "weighted_out", where_clause="VALUE = " + str(Value_Max))
    outCon.save("conditioned_out")




    print "Condictional Filter Completed"
    # Make a majority filter for the result of conditional evaluation.
    # Then save the result of majority filter in geodatabase.(almost 2 lines)

    # Using low-pass filter (Majority) to get more general boundary instead of "salt and pepper" cell
    outMajFilt = MajorityFilter(outCon, "EIGHT", "MAJORITY")
    outMajFilt.save("filtered_out")



    print "Majority Filter Completed"

    # Convert the result of majority filter(raster) to polygon feature class. (almost 1 line)
    # Convert it to polygon
    arcpy.RasterToPolygon_conversion(outMajFilt, "polygon_class", "SIMPLIFY", "VALUE")

    # Create a feature layer from the polygon feature class. Select Layer By Location and Attribute under some certeria.
    # (almost 3 lines)

    # Using layer to select the best location
    arcpy.MakeFeatureLayer_management("polygon_class", "polygon")

    arcpy.SelectLayerByLocation_management("polygon", "INTERSECT", Input_File["roads"], selection_type="NEW_SELECTION")
    arcpy.SelectLayerByAttribute_management("polygon", "SUBSET_SELECTION", "\"Shape_Area\">=40469")

    print "Final Feature Selection: Completed"
    # Copy the selected layed to a new polygon feature class. (almost 1 line)

    # Output the final product class
    arcpy.CopyFeatures_management("polygon",Final_Site)


    print "Selected Final School Site! "


def Scaled_Value(Reclass_Level, RMV):
    '''
    This function is to further filter out cells with particular characteristics. For example, for the slope dataset, the
    cells with values equal or smaller than 3 will be set to "restricted", which means those cells are not suitable locations.
    If the cell has a value of 'NODATA', it will be remapped to the same value, i.e., 'NODATA'. (hint: using ["NODATA", "NODATA"]).

    :param Reclass_Level:  A number describing how many levels are used to distinguish the suitability of each pixel;
    :param RMV: The initialized remap values(1-dimensional list) for different datasets, e.g., Slp_remapvalue, Sch_remapvalue, Rec_remapvalue.
    :return: A 2-dimensional list, with each element showing the value before and after
             the remapping operation. (e.g., [[0, 0],[1, 'restricted'], ...['NODATA', 'NODATA']])
    '''

    RMV_List = []
    for i in range(Reclass_Level):
        RMV_List.append([i + 1, RMV[i]])
    RMV_List.append(["NODATA", "NODATA"])
    return RMV_List



if __name__ == '__main__':

    # Statement of the Remap value of Slope, Distance of school and Recreation.
    Slope_remapvalue, Sch_remapvalue, Rec_remapvalue = [], [], []

    # Set the Level of Reclassification.
    Reclass_Level = 10

    # This dictionary with key as data name(inputs of overlaying), and the value as the associated influence value.
    Influence_Val = {
        "slope": 20, #13,
        "rec_sites": 33, #50,
        "schools": 25,
        "landuse": 22 #12
    }

    # The dictionary with key as data type(input file), and the value as the associated file name.
    Input_File = {
        "DEM": "elevation",
        "landuse": "landuse",
        "rec_sites": "rec_sites",
        "schools": "schools",
        "roads": "roads"
    }

    # The dictionary with key as data type(derived datasets), and the value as the associated file name.
    Slope_Dist_Output = {
        "slope": "slope",
        "schools": "school_dis",
        "rec_sites": "rec_dis"
    }

    # The dictionary with key as data type(reclassified datasets), and the value as the associated file name.
    Reclass_Dict = {
        "slope": "slope_reclass",
        "schools": "school_reclass",
        "rec_sites": "recreation_reclass"
    }

    # The dictionary contains the remap value of different land use types.
    Landuse_rmv = {
        "Brush/transitional": 5,
        "Water": "Restricted",
        "Barren_land": 10,
        "Built_up": 5, #3,
        "Agriculture": 6, #9,
        "Forest": 9, #4,
        "Wetlands": "Restricted"
    }

    # This for loop is for initializing remap value for slope, the distance of school and the distance of recreational sites.
    for i in range(Reclass_Level):
        Slope_remapvalue.append(i + 1)
        Sch_remapvalue.append(i + 1)
        Rec_remapvalue.append(i + 1)

    Slope_remapvalue[0] = "Restricted"
    Slope_remapvalue[1] = "Restricted"
    Slope_remapvalue[2] = "Restricted"

    # The polygon name of Final School Site.
    Final_Site = "Final_Site"


    Distance_Slope(Input_File, Slope_Dist_Output)
    Reclassification(Slope_Dist_Output, Reclass_Dict, Reclass_Level)
    Weighted_Overlay(Input_File, Reclass_Dict, Influence_Val, Slope_remapvalue, Sch_remapvalue, Rec_remapvalue, Landuse_rmv)

    Filter_FinalSite(Final_Site, Input_File)
    arcpy.CheckInExtension("Spatial")
