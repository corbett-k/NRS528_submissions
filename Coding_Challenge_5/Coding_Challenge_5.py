## Coding Challenge 5 ##

import arcpy, csv

# set the workspace / .csv file location
arcpy.env.workspace = r"C:\Users\Kristopher\Documents\NRS528_submissions_REPO\Coding_Challenge_5"


# first determine what species are contained in the CSV

species = []
filename = "species_combined_dataset.csv"

with open(filename) as spp_csv:
    next(spp_csv)  # skips first line (column headings)

    for row in csv.reader(spp_csv):
        if row[0] not in species:
            species.append(row[0])

    print("\nYour dataset contains the following list of species:")
    print(species)

    # Next, create a shapefile for all species, then perform a selection for every species and output a layer
    # for each individual species

for s in species:

    # first create a layer encompassing the entire .csv dataset
    in_Table = spp_csv
    x_coords = "longitude"
    y_coords = "latitude"
    z_coords = ""
    out_Layer = "all_species"
    spRef = arcpy.SpatialReference(4326)  # including the spatial reference (4326 == WGS 1984)

    arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

    # list the total number of rows for the all_species layer
    row_ttl = arcpy.GetCount_management(out_Layer)
    print("\nThe dataset contains " + str(row_ttl) + " rows of data.")

    # select individual species with the all_species layer
    sp_selection = arcpy.SelectLayerByAttribute_management(out_Layer, "NEW_SELECTION", "species = " + s)

    # create a unique shapefile layer for each species
    sp_layer = "sp_lyr_" + s
    arcpy.CopyFeatures_management(sp_selection, sp_layer)

    # determine that shapefile has been created
    if arcpy.Exists(sp_layer):
        print("A shapefile for " + s + " has been created ...\n")

    # describe the extent of each species shapefile
    desc = arcpy.Describe(sp_layer)
    XMin = desc.extent.XMin
    XMax = desc.extent.XMax
    YMin = desc.extent.YMin
    YMax = desc.extent.YMax

    print("The spatial extent for the distribution of species: " + s)
    print("XMin: " + str(XMin) + "\nXMax: " + str(XMax) + "\nYMin: " + str(YMin) + "\nYMax: " + str(YMax))

    # Create a fishnet for the shapefile
    outFeatureClass = "sp_fishnet" + s + ".shp"
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

    # perform spatial join of shapefile and fishnet to create heatmap
    target_features = outFeatureClass
    join_features = sp_layer
    out_feature_class = "heatmap_" + s + ".shp"
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
        print("\nHeatmap for " + s + " successfully generated.")

# inform that all heatmaps have been created successfully
print("\nAll species heatmap shapefiles are ready. These can now be open and viewed in ArcGIS Pro.\n "
      "Be sure to change Symbology to 'Graduated Colors' and adjust # of classes accordingly.")

# delete intermediary files

