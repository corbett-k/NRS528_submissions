## Coding Challenge 7 ##

import os, arcpy, csv, glob

data_file = "species_combined_dataset.csv"
input_directory = r"C:\Users\Kristopher\Documents\NRS528_submissions_REPO\Coding_Challenge_7"

if not os.path.exists(os.path.join(input_directory, "output_files")):
    os.mkdir(os.path.join(input_directory, "output_files"))
if not os.path.exists(os.path.join(input_directory, "temporary_files")):
    os.mkdir(os.path.join(input_directory, "temporary_files"))

# first determine what species are contained in the .csv file

species_list = []

with open(os.path.join(input_directory, data_file)) as spp_csv:
    header_line = next(spp_csv)  # skips first line (column headings)
    try:
        for row in csv.reader(spp_csv):
            if row[0] not in species_list:
                species_list.append(row[0])
    except:
        pass

print("\nThere are " + str(len(species_list)) + " species in your dataset to process...")
print("\nThe dataset contains the following list of species:\n" + str(species_list) + "\n")

if len(species_list) > 1:
    for sp in species_list:
        sp_count = 1
        with open(os.path.join(input_directory, data_file)) as species_csv:
            for row in csv.reader(species_csv):
                if row[0] == sp:
                    if sp_count == 1:
                        file = open(os.path.join(input_directory, "temporary_files", str(sp.replace(" ", "_")) + ".csv"), "w")
                        file.write(header_line)
                        sp_count = 0
                    file.write(",".join(row))
                    file.write("\n")
        file.close()

os.chdir(os.path.join(input_directory, "temporary_files"))
arcpy.env.workspace = os.path.join(input_directory, "output_files")
species_file_list = glob.glob("*.csv")

count = 0

for sp_file in species_file_list:
    print("Processing '" + str(sp_file) + "' by converting to shapefile format...")

    in_Table = sp_file
    x_coords = "longitude"
    y_coords = "latitude"
    z_coords = ""
    out_Layer = "species_" + str(count)
    spRef = arcpy.SpatialReference(4326)  # including the spatial reference (4326 == WGS 1984)

    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)
    saved_Layer = sp_file.replace('.csv','') + ".shp"
    arcpy.CopyFeatures_management(lyr, saved_Layer)

    if arcpy.Exists(saved_Layer):
        print("Shapefile generated for species: '" + sp_file + "'.")
    arcpy.Delete_management(lyr)

    # describe the extent of each species shapefile
    desc = arcpy.Describe(saved_Layer)
    XMin = desc.extent.XMin
    XMax = desc.extent.XMax
    YMin = desc.extent.YMin
    YMax = desc.extent.YMax

    print("Spatial extent of '" + sp_file + "' shapefile:\nXMin: " + str(XMin) + "\nXMax: " + str(XMax) + "\nYMin: "
          + str(YMin) + "\nYMax: " + str(YMax))

    # create a fishnet for the shapefile
    outFeatureClass = "fishnet_" + sp_file
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
        print("Fishnet generated based on '" + sp_file + "' shapefile's extent...")

    # perform spatial join of shapefile and fishnet to create heatmap
    target_features = outFeatureClass
    join_features = saved_Layer
    out_feature_class = "heatmap_" + sp_file
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
        print("Heatmap for '" + sp_file + "' successfully generated.\n")

    count = count + 1

arcpy.Delete_management(os.path.join(input_directory, "temporary_files"))
print("All intermediate files deleted.")

print("\n--------------------------------------------\n")
# confirm all heatmaps have been created successfully
print("All species heatmaps have been successfully generated.\nThese can now be opened and viewed in ArcGIS.\n"
      "(tip: change Symbology to 'Graduated Colors' and adjust # of classes accordingly.")
