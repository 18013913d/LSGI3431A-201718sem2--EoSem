import arcpy
import os

arcpy.CheckOutExtension("Spatial")
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

reclass = 10

influence = {
    'feature': 65,
    'MTR': 10,
    'building': 12,
    'road': 8,
    'population density': 5
}

reverse_table = []

for i in range(0, reclass):
    reverse_table.append([i + 1, reclass - i])

if __name__ == '__main__':
    print "Please input the path for your gdb with all facilities:"
    gdb_name = raw_input(">>> ")

    if gdb_name == "":
        os.write(2, "[ERROR] You haven't type the name of your gdb! Exiting...\n")
        exit(1)

    if not gdb_name.endswith(".gdb"):
        gdb_name += ".gdb"

    cwd = os.getcwd()
    if not os.path.isabs(gdb_name):
        print "[INFO] Convert it to absolute by using the path for the script"
        print "[INFO] i.e. %s" % os.path.realpath(os.path.join(cwd, gdb_name))
        gdb_name = os.path.realpath(os.path.join(cwd, gdb_name))

    arcpy.env.workspace = gdb_name
    arcpy.env.extent = arcpy.Describe("HK_adm_1980").extent
    arcpy.env.cellsize = "300"

    in_polygons = "HK_adm_1980"
    hk_pop_den_raster = "HK_pop_den"
    pop_den_reclassed = "HK_den_class"

    try:
        arcpy.Delete_management("HK_single_polygon")
    except:
        pass

    arcpy.Dissolve_management(in_polygons, "HK_single_polygon")

    # Initializing Population density raster

    try:
        arcpy.Delete_management(hk_pop_den_raster)
    except:
        pass
    try:
        arcpy.Delete_management(pop_den_reclassed)
    except:
        pass

    density_field = 'Pop_Density'
    try:
        arcpy.PolygonToRaster_conversion(in_polygons, density_field, hk_pop_den_raster)
    except:
        # Shapefile Compatibility
        arcpy.PolygonToRaster_conversion(in_polygons, 'Pop_Densit', hk_pop_den_raster)

    arcpy.sa.Slice(hk_pop_den_raster, reclass, "NATURAL_BREAKS").save(pop_den_reclassed)

    try:
        arcpy.Delete_management('MTR_dist')
    except:
        pass
    try:
        arcpy.Delete_management('bldg_temp')
    except:
        pass
    try:
        arcpy.Delete_management('bldg_den')
    except:
        pass
    try:
        arcpy.Delete_management('road_dist')
    except:
        pass

    try:
        arcpy.Delete_management('MTR_reclassed')
    except:
        pass
    try:
        arcpy.Delete_management('bldg_reclassed')
    except:
        pass
    try:
        arcpy.Delete_management('road_reclassed')
    except:
        pass

    MTR = 'MTR_stop'
    try:
        arcpy.CopyFeatures_management('../All_MTR_stop.shp', MTR)
    except:
        pass

    arcpy.sa.EucDistance(MTR).save('MTR_dist')
    outSlice = arcpy.sa.Slice('MTR_dist', reclass, "EQUAL_INTERVAL")
    outreclass = arcpy.sa.Reclassify(outSlice, "Value", arcpy.sa.RemapValue(reverse_table))
    outreclass.save('MTR_reclassed')

    building = 'bldg'
    try:
        arcpy.CopyFeatures_management('../HK_Bldg.shp', building)
    except:
        pass
    arcpy.FeatureToPoint_management(building, "bldg_temp", "CENTROID")
    arcpy.sa.KernelDensity('bldg_temp', "NONE", cell_size=100,
                           area_unit_scale_factor="SQUARE_KILOMETERS").save('bldg_den')
    outSlice = arcpy.sa.Slice('bldg_den', reclass, "EQUAL_INTERVAL")
    outreclass.save('bldg_reclassed')

    road = 'road_centerline'
    try:
        arcpy.CopyFeatures_management('../CENTRELINE.mdb/CENTRELINE', road)
    except:
        pass
    arcpy.sa.EucDistance(road, 3500).save('road_dist')
    outSlice = arcpy.sa.Slice('road_dist', reclass, "EQUAL_INTERVAL")
    outreclass = arcpy.sa.Reclassify(outSlice, "Value", arcpy.sa.RemapValue(reverse_table))
    outreclass.save('road_reclassed')

    try:
        arcpy.Delete_management('bldg_temp')
    except:
        pass
    """
    try:
        arcpy.Delete_management('bldg_den')
    catch:
        pass
    """

    del outSlice
    del outreclass

    try:
        arcpy.Delete_management(hk_pop_den_raster)
    except:
        pass

    for join_features in name.iterkeys():
        # By District
        output = "%s_output" % join_features
        join_operation = 'JOIN_ONE_TO_ONE'

        join_type = 'KEEP_ALL'
        match_option = 'CONTAINS'

        try:
            arcpy.Delete_management(output)
        except:
            pass
        arcpy.SpatialJoin_analysis(in_polygons, join_features, output, join_operation, join_type, match_option)

        print "Coverage Data by district written for type %s" % name[join_features]

        # Now Create Kernel Density
        populationField = "NONE"

        result = arcpy.GetCount_management(join_features)

        output_dens = arcpy.sa.KernelDensity(join_features, populationField, cell_size=100,
                                             area_unit_scale_factor="SQUARE_KILOMETERS")
        try:
            arcpy.Delete_management(join_features + "_density")
        except:
            pass

        arcpy.Clip_management(output_dens, "800000 800000 860000 848000", join_features + "_density",
                              in_template_dataset=in_polygons, clipping_geometry="ClippingGeometry",
                              maintain_clipping_extent="MAINTAIN_EXTENT")

        print 'Kernel Density for type %s finished' % name[join_features]
        print 'Density point pattern analysis finished.'

        # Now Calculated Ripley K

        arcpy.MakeFeatureLayer_management(join_features, join_features + "_lyr")
        arcpy.MultiDistanceSpatialClustering_stats(join_features + "_lyr", join_features + "_lyr.dbf", 15,
                                                   "99_PERMUTATIONS",
                                                   "DISPLAY_IT", "#",
                                                   Boundary_Correction_Method="SIMULATE_OUTER_BOUNDARY_VALUES",
                                                   Study_Area_Method="MINIMUM_ENCLOSING_RECTANGLE",
                                                   Study_Area_Feature_Class="HK_single_polygon")
        print "Ripley K for type %s finished" % name[join_features]
        print "Distance point pattern analysis finished."

        # Find the area with good coverage
        try:
            arcpy.Delete_management(join_features + "_den")
        except:
            pass

        # Derive class table

        reverse_table = []

        for i in range(0, reclass):
            reverse_table.append([i + 1, reclass - i])

        arcpy.sa.Slice(join_features + "_density", reclass, "EQUAL_INTERVAL").save(join_features + "_class")

        try:
            arcpy.Delete_management(join_features + "_den")
        except:
            pass

        try:
            arcpy.Delete_management(join_features + "_weight")
        except:
            pass

        reverse_table.append(["NODATA", "NODATA"])

        normal_list = [[i, i] for i in range(1, reclass + 1)]
        outSuit = arcpy.sa.WOTable(
            [[join_features + "_class", influence['feature'], "VALUE", arcpy.sa.RemapValue(normal_list)],
             [pop_den_reclassed, influence["population density"], "VALUE", arcpy.sa.RemapValue(normal_list)],
             ['MTR_reclassed', influence['MTR'], "VALUE", arcpy.sa.RemapValue(normal_list)],
             ['bldg_reclassed', influence['building'], "VALUE", arcpy.sa.RemapValue(normal_list)],
             ['road_reclassed', influence['road'], "VALUE", arcpy.sa.RemapValue(normal_list)]],
            [1, reclass, 1])
        outWeightedOverlay = arcpy.sa.WeightedOverlay(outSuit)
        outWeightedOverlay.save(join_features + "_weight")
        """
        try:
            arcpy.Delete_management("MTR_reclassed")
        except:
            pass

        try:
            arcpy.Delete_management("bldg_reclassed")
        except:
            pass
        """

        try:
            arcpy.Delete_management(join_features + "_class")
        except:
            pass

        # Get the highest value we could found
        Value_Max = arcpy.GetRasterProperties_management(join_features + "_weight", "MAXIMUM")
        outCon = arcpy.sa.Con(join_features + "_weight", join_features + "_weight",
                              where_clause="VALUE IN( " + Value_Max.getOutput(0) + "," + str(
                                  int(Value_Max.getOutput(0)) - 1) + ")")

        del Value_Max
        # Make a majority filter for the result of conditional evaluation.

        # Using low-pass filter (Majority) to get more general boundary instead of "salt and pepper" cell
        outMajFilt = arcpy.sa.MajorityFilter(outCon, "EIGHT", "MAJORITY")

        # Convert the result of majority filter(raster) to polygon feature class. (almost 1 line)
        # Convert it to polygon
        try:
            arcpy.Delete_management(join_features + "_polygon")
        except:
            pass

        arcpy.RasterToPolygon_conversion(outMajFilt, join_features + "_polygon", "SIMPLIFY", "VALUE")

        # Create a feature layer from the polygon feature class. Select Layer By Location and Attribute under some certeria.

        # Using layer to select the best location
        arcpy.MakeFeatureLayer_management(join_features + "_polygon", "polygon_lyr")
        arcpy.SelectLayerByAttribute_management("polygon_lyr", "NEW_SELECTION", "\"Shape_Area\">=200")

        print "Final Feature Selection: Completed"
        # Copy the selected layed to a new polygon feature class. (almost 1 line)

        # Output the final product class
        try:
            arcpy.Delete_management(join_features + "_prefinal")
        except:
            pass
        try:
            arcpy.Delete_management(join_features + "_final")
        except:
            pass
        arcpy.CopyFeatures_management("polygon_lyr", join_features + "_prefinal")
        arcpy.Dissolve_management(join_features + "_prefinal", join_features + "_final")
        try:
            arcpy.Delete_management(join_features + "_prefinal")
        except:
            pass

        try:
            arcpy.Delete_management(join_features + "_polygon")
        except:
            pass

        print "Good coverage of site %s selected" % name[join_features]


