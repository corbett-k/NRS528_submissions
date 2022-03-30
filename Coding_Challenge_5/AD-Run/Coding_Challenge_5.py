## Coding Challenge 5 ##

import csv
import arcpy

# set the workspace
arcpy.env.workspace = r"C:\Data\Students_2022\Corbett\Coding_Challenge_5\AD-Run"

# first determine what species are contained in the CSV

species = []

with open(r"C:\Data\Students_2022\Corbett\Coding_Challenge_5\AD-Run"
          r"\species_combined_dataset.csv") as spp_csv:
    next(spp_csv) #skips first line (column headings)

    for row in csv.reader(spp_csv):
        if row[0] not in species:
            species.append(row[0])

print("\nYour dataset contains the following list of species:")
print(species)

# request filename:
filename = input("\nWhat is the name of the file containing your dataset? ")

in_Table = filename
x_coords = "longitude"
y_coords = "latitude"
z_coords = ""
out_Layer = "all_species"
saved_Layer = r"all_spp.shp"

# Set the spatial reference
spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984

# Creating the XY Event Layer
lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

# list the total number of rows
row_ttl = arcpy.GetCount_management(out_Layer)
print("\nThe dataset contains " + str(row_ttl) + " rows of data.")

# Save to a layer file
arcpy.CopyFeatures_management(lyr, saved_Layer)

# Determine that shapefile has been created
if arcpy.Exists(saved_Layer):
    print("A shapefile containing all rows of species data has been created successfully...\n")

# # select by species to create independent shapefiles

sp1_lyr = r"species_1_output.shp"
sp2_lyr = r"species_2_output.shp"

sp_select_1 = arcpy.SelectLayerByAttribute_management(saved_Layer, "NEW_SELECTION", "species = '" + species[0] + "'")
arcpy.CopyFeatures_management(sp_select_1, sp1_lyr)

if arcpy.Exists(sp1_lyr):
    print("A shapefile for species #1 has been created successfully...\n")

sp_select_2 = arcpy.SelectLayerByAttribute_management(saved_Layer, "NEW_SELECTION", "species = '" + species[1] + "'")
arcpy.CopyFeatures_management(sp_select_2, sp2_lyr)

if arcpy.Exists(sp2_lyr):
    print("A shapefile for species #2 has been created successfully...\n")

desc = arcpy.Describe(sp1_lyr)
XMin1 = desc.extent.XMin
XMax1 = desc.extent.XMax
YMin1 = desc.extent.YMin
YMax1 = desc.extent.YMax

print("The spatial extent for the distribution of species 1:")
print("XMin: " + str(XMin1) + "\nXMax: " + str(XMax1) + "\nYMin: " + str(YMin1) + "\nYMax: " + str(YMax1))

desc = arcpy.Describe(sp2_lyr)
XMin2 = desc.extent.XMin
XMax2 = desc.extent.XMax
YMin2 = desc.extent.YMin
YMax2 = desc.extent.YMax

print("\nThe spatial extent for the distribution of species 2:")
print("XMin: " + str(XMin2) + "\nXMax: " + str(XMax2) + "\nYMin: " + str(YMin2) + "\nYMax: " + str(YMax2))

#create fishnets

outFeatureClass_sp1 = "sp1_fishnet.shp"
originCoordinate_sp1 = str(XMin1) + " " + str(YMin1)
yAxisCoordinate_sp1 = str(XMin1) + " " + str(YMin1 + 1.0)
cellSizeWidth_sp1 = "2"
cellSizeHeight_sp1 = "2"
numRows_sp1 = ""
numColumns_sp1 = ""
oppositeCorner_sp1 = str(XMax1) + " " + str(YMax1)
labels_sp1 = "NO_LABELS"
templateExtent_sp1 = "#"
geometryType_sp1 = "POLYGON"

arcpy.CreateFishnet_management(outFeatureClass_sp1, originCoordinate_sp1, yAxisCoordinate_sp1,
                               cellSizeWidth_sp1, cellSizeHeight_sp1, numRows_sp1, numColumns_sp1,
                               oppositeCorner_sp1, labels_sp1, templateExtent_sp1, geometryType_sp1)

outFeatureClass_sp2 = "sp2_fishnet.shp"
originCoordinate_sp2 = str(XMin2) + " " + str(YMin2)
yAxisCoordinate_sp2 = str(XMin2) + " " + str(YMin2 + 1.0)
cellSizeWidth_sp2 = "2"
cellSizeHeight_sp2 = "2"
numRows_sp2 = ""
numColumns_sp2 = ""
oppositeCorner_sp2 = str(XMax2) + " " + str(YMax2)
labels_sp2 = "NO_LABELS"
templateExtent_sp2 = "#"
geometryType_sp2 = "POLYGON"

arcpy.CreateFishnet_management(outFeatureClass_sp2, originCoordinate_sp2, yAxisCoordinate_sp2,
                               cellSizeWidth_sp2, cellSizeHeight_sp2, numRows_sp2, numColumns_sp2,
                               oppositeCorner_sp2, labels_sp2, templateExtent_sp2, geometryType_sp2)

# perform spatial joins

target_features_sp1 = outFeatureClass_sp1
join_features_sp1 = sp1_lyr
out_feature_class_sp1 = "sp1_HeatMap.shp"
join_operation_sp1 = "JOIN_ONE_TO_ONE"
join_type_sp1 = "KEEP_ALL"
field_mapping_sp1 = ""
match_option_sp1 = "INTERSECT"
search_radius_sp1 = ""
distance_field_name_sp1 = ""

arcpy.SpatialJoin_analysis(target_features_sp1, join_features_sp1, out_feature_class_sp1,
                           join_operation_sp1, join_type_sp1, field_mapping_sp1, match_option_sp1,
                           search_radius_sp1, distance_field_name_sp1)

if arcpy.Exists(out_feature_class_sp1):
    print("\nSpecies 1 heatmap created successfully.")

target_features_sp2 = outFeatureClass_sp2
join_features_sp2 = sp2_lyr
out_feature_class_sp2 = "sp2_HeatMap.shp"
join_operation_sp2 = "JOIN_ONE_TO_ONE"
join_type_sp2 = "KEEP_ALL"
field_mapping_sp2 = ""
match_option_sp2 = "INTERSECT"
search_radius_sp2 = ""
distance_field_name_sp2 = ""

arcpy.SpatialJoin_analysis(target_features_sp2, join_features_sp2, out_feature_class_sp2,
                           join_operation_sp2, join_type_sp2, field_mapping_sp2, match_option_sp2,
                           search_radius_sp2, distance_field_name_sp2)

if arcpy.Exists(out_feature_class_sp2):
    print("Species 2 heatmap created successfully.")

print("\nopen heatmap shapefiles in ArcGIS Pro, change symbology to 'Graduated Colors' (using 10 classes)")