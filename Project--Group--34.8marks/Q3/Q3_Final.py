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
    'MTR': 18,
    'building': 55,
    'road': 17,
    'population density': 10
}

reverse_table = []

for i in range(0,reclass):
    reverse_table.append([i+1,reclass-i])

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

    populationField = "NONE"
    i = 0
    raster_list = []

    density_field = 'Pop_Density'
    hk_pop_den_raster = "HK_pop_den"
    pop_den_reclassed = "HK_den_class"

    try:
        arcpy.Delete_management(hk_pop_den_raster)
    except:
        pass
    try:
        arcpy.Delete_management(pop_den_reclassed)
    except:
        pass

    try:
        arcpy.PolygonToRaster_conversion("HK_adm_1980", density_field, hk_pop_den_raster)
    except:
        # Shapefile Compatibility
        arcpy.PolygonToRaster_conversion("HK_adm_1980", 'Pop_Densit', hk_pop_den_raster)

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
    try:
        arcpy.Delete_management(hk_pop_den_raster)
    except:
        pass

    for raster in name.iterkeys():
        try:
            arcpy.Delete_management("outslice_"+raster)
        except:
            pass


    for join_features in name.iterkeys():
        i += 1

        try:
            arcpy.Delete_management(join_features+"_dist")
        except:
            pass

        eucRaster = arcpy.sa.EucDistance(join_features, 5000.0, cell_size=300)
        eucRaster.save("eucRas")
        outSlice_rec = arcpy.sa.Slice("eucRas", 1, "EQUAL_INTERVAL")
        arcpy.Delete_management("eucRas")
        outSlice_rec.save("outslice_"+join_features)

        del eucRaster
        del outSlice_rec

    try:
        arcpy.Delete_management("temp_raster")
    except:
        pass

    try:
        arcpy.Delete_management("final_gt3_fac")
    except:
        pass

    raster_list = ["outslice_"+raster for raster in name.iterkeys()]
    last_raster = arcpy.sa.CellStatistics(raster_list, "SUM", "DATA")
    last_raster.save("temp_raster")
    outCon = arcpy.sa.Con("temp_raster", "temp_raster", where_clause="VALUE >= 3")
    arcpy.Clip_management(outCon, "800000 800000 860000 848000", "final_gt3_fac",
                          in_template_dataset="HK_adm_1980", clipping_geometry="ClippingGeometry",
                          maintain_clipping_extent="MAINTAIN_EXTENT")
    """
    try:
        arcpy.Delete_management("temp_raster")
    except:
        pass
    """
    normal_list = [[i, i] for i in range(1, reclass + 1)]
    outSuit = arcpy.sa.WOTable(
        [[pop_den_reclassed, influence["population density"], "VALUE", arcpy.sa.RemapValue(normal_list)],
         ['MTR_reclassed', influence['MTR'], "VALUE", arcpy.sa.RemapValue(normal_list)],
         ['bldg_reclassed', influence['building'], "VALUE", arcpy.sa.RemapValue(normal_list)],
         ['road_reclassed', influence['road'], "VALUE", arcpy.sa.RemapValue(normal_list)]],
        [1, reclass, 1])
    outWeightedOverlay = arcpy.sa.WeightedOverlay(outSuit)
    try:
        outWeightedOverlay.save("urban")
    except:
        arcpy.Delete_management("urban")
        outWeightedOverlay.save("urban")
    for raster in name.iterkeys():
        try:
            arcpy.Delete_management("outslice_"+raster)
        except:
            pass
    try:
        arcpy.Delete_management("final_urban_gt3_fac")
    except:
        pass

    Value_Max = arcpy.GetRasterProperties_management("urban", "MAXIMUM").getOutput(0)
    outCon_urban = arcpy.sa.Con("urban", "urban",
                          where_clause="VALUE IN(" + Value_Max +", " + str(int(Value_Max)-1) + ")")
    try:
        arcpy.sa.MajorityFilter(outCon_urban, "EIGHT", "MAJORITY").save("filter_urban")
    except:
        arcpy.Delete_management("filter_urban")
        arcpy.sa.MajorityFilter(outCon_urban, "EIGHT", "MAJORITY").save("filter_urban")
    try:
        arcpy.RasterToPolygon_conversion("filter_urban", "urban_polygon", "SIMPLIFY", "VALUE")
    except:
        arcpy.Delete_management("urban_polygon")
        arcpy.RasterToPolygon_conversion("filter_urban", "urban_polygon", "SIMPLIFY", "VALUE")

    arcpy.Clip_management(outCon, "800000 800000 860000 848000", "final_urban_gt3_fac",
                          in_template_dataset="urban_polygon", nodata_value="NODATA",
                          clipping_geometry="ClippingGeometry", maintain_clipping_extent="MAINTAIN_EXTENT")
    """
    try:
        arcpy.Delete_management("filter_urban")
    except:
        pass
    """

    for raster in name.iterkeys():
        try:
            arcpy.Delete_management("outslice_"+raster)
        except:
            pass
    del last_raster
    del outCon
    print "Good coverage of more than three facilities selected"
    del arcpy