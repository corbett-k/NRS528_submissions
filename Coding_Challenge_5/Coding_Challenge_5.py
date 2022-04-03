## Coding Challenge 5 ##

import arcpy, csv

# set the workspace / .csv file location
arcpy.env.workspace = r"C:\Users\Kristopher\Documents\NRS528_submissions_REPO\Coding_Challenge_5"


# first determine what species are contained in the .csv file
species_list = []

with open(r"species_combined_dataset.csv") as spp_csv:
    next(spp_csv)  # skips first line (column headings)

    for row in csv.reader(spp_csv):
        if row[0] not in species_list:
            species_list.append(row[0])

    print("\nYour dataset contains the following list of species:")
    print(species_list)

# create a layer encompassing the entire .csv dataset
in_Table = "species_combined_dataset.csv"
x_coords = "longitude"
y_coords = "latitude"
z_coords = ""
out_Layer = "all_species.shp"
spRef = arcpy.SpatialReference(4326)  # including the spatial reference (4326 == WGS 1984)

arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

if arcpy.Exists(out_Layer):
    print("\nA layer containing all species data exists...")
#
# total number of rows
row_ttl = arcpy.GetCount_management(out_Layer)
print("This dataset contains " + str(row_ttl) + " rows.\n")

copy_layer = "copy_layer.shp"
arcpy.CopyFeatures_management(out_Layer, copy_layer)

# verify all_species shapefile created
if arcpy.Exists(copy_layer):
    print("A shapefile containing all species data has been generated...\n")

# loop through all species and generate relevant files (shapefile, fishnet) to generate a heatmap

for sp in species_list:

    # select individual species with the all_species layer
    # arcpy.management.SelectLayerByAttribute(in_layer_or_view, {selection_type}, {where_clause}, {invert_where_clause})

    sp_selection = arcpy.SelectLayerByAttribute_management(copy_layer, "NEW_SELECTION", "species = '" + sp + "'")

    # create a unique shapefile layer for each species
    sp_layer = "sp_lyr_" + sp + ".shp"
    arcpy.CopyFeatures_management(sp_selection, sp_layer)

    # determine that shapefile has been created
    if arcpy.Exists(sp_layer):
        print("Shapefile generated for species: '" + sp + "'")

    # describe the extent of each species shapefile
    desc = arcpy.Describe(sp_layer)
    XMin = desc.extent.XMin
    XMax = desc.extent.XMax
    YMin = desc.extent.YMin
    YMax = desc.extent.YMax

    print("Spatial extent of '" + sp + "' shapefile:\nXMin: " + str(XMin) + "\nXMax: " + str(XMax) + "\nYMin: "
          + str(YMin) + "\nYMax: " + str(YMax))

    # create a fishnet for the shapefile
    outFeatureClass = "sp_fishnet_" + sp + ".shp"
    originCoordinate = str(XMin) + " " + str(YMin)
    yAxisCoordinate = str(XMin) + " " + str(YMin + 1.0)
    cellSizeWidth = "2"
    cellSizeHeight = "2"
    numRows = ""
    numColumns = ""
    oppositeCorner = str(XMax) + " " + str(YMax)
    labels = "NO_LABELS"
    templateExtent = "#"
    geometryType = "POLYGON"

    arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                                   cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                   oppositeCorner, labels, templateExtent, geometryType)

    if arcpy.Exists(outFeatureClass):
        print("Fishnet generated based on '" + sp + "' shapefile's extent...")

    # perform spatial join of shapefile and fishnet to create heatmap
    target_features = outFeatureClass
    join_features = sp_layer
    out_feature_class = "heatmap_" + sp + ".shp"
    join_operation = "JOIN_ONE_TO_ONE"
    join_type = "KEEP_ALL"
    field_mapping = ""
    match_option = "INTERSECT"
    search_radius = ""
    distance_field_name = ""

    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                               join_operation, join_type, field_mapping, match_option,
                               search_radius, distance_field_name)

    # ensure heatmap has been created
    if arcpy.Exists(out_feature_class):
        print("Heatmap for '" + sp + "' successfully generated.\n")

    # clean up intermediate files
    arcpy.Delete_management(sp_layer)
    arcpy.Delete_management(outFeatureClass)

arcpy.Delete_management(copy_layer)
print("All intermediate files deleted.")

print("\n--------------------------------------------\n")
# confirm all heatmaps have been created successfully
print("All species heatmaps have been successfully generated.\nThese can now be opened and viewed in ArcGIS.\n"
      "(tip: change Symbology to 'Graduated Colors' and adjust # of classes accordingly.")
