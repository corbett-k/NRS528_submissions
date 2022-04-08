### CODING CHALLENGE VIII ###


import os, arcpy, csv, glob

from colorama import Fore, Back, Style

data_file = "species_combined_dataset.csv"
input_directory = r"C:\Users\Kristopher\Documents\NRS-528_submissions_Repo\Coding_Challenge_8"

if not os.path.exists(os.path.join(input_directory, "output_files")):
    os.mkdir(os.path.join(input_directory, "output_files"))
# if not os.path.exists(os.path.join(input_directory, "temporary_files")):
#     os.mkdir(os.path.join(input_directory, "temporary_files"))

arcpy.env.workspace = os.path.join(input_directory, "output_files")

def species_heatmap(species_file_list):
    for sp_list in species_file_list:

        print("\nConverting " + Fore.BLACK + Back.WHITE + sp_list + Style.RESET_ALL + " from table to shapefile format...")

        sp = str(sp_list).replace(".csv", "")

        in_Table = str(sp_list)
        x_coords = "longitude"
        y_coords = "latitude"
        z_coords = ""
        out_Layer = str(sp)
        spRef = arcpy.SpatialReference(4326)  # including the spatial reference (4326 == WGS 1984)

        lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

        saved_Layer = str(sp) + "_shapefile.shp"

        if arcpy.Exists(saved_Layer):
            arcpy.Delete_management(saved_Layer)

        arcpy.CopyFeatures_management(lyr, saved_Layer)

        if arcpy.Exists(saved_Layer):
            print(Fore.MAGENTA + "Shapefile" + Fore.RESET + " generated for species '" + sp + "'.")
        arcpy.Delete_management(lyr)

        # describe spatial extent of species shapefile
        desc = arcpy.Describe(saved_Layer)
        XMin = desc.extent.XMin
        XMax = desc.extent.XMax
        YMin = desc.extent.YMin
        YMax = desc.extent.YMax

        print(saved_Layer + " spatial extent:" + "\nXMin:" + str(XMin) + " XMax:" + str(XMax) +
                            "  YMin:"+ str(YMin) + "  YMax:" + str(YMax))

        # create fishnet for species shapefile based on spatial extent values and appropriate cell size, # of rows/columns
        outFeatureClass = out_Layer + "_fishnet.shp"
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

        if arcpy.Exists(outFeatureClass):
            arcpy.Delete_management(outFeatureClass)

        arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                                       cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                       oppositeCorner, labels, templateExtent, geometryType)

        if arcpy.Exists(outFeatureClass):
            print(Fore.BLUE + "Fishnet" + Fore.RESET + " generated using spatial extent of '" + sp + "' shapefile.")

        # perform spatial join of shapefile and fishnet to create heatmap
        target_features = outFeatureClass
        join_features = saved_Layer
        out_feature_class = sp + "_heatmap.shp"
        join_operation = "JOIN_ONE_TO_ONE"
        join_type = "KEEP_ALL"
        field_mapping = ""
        match_option = "INTERSECT"
        search_radius = ""
        distance_field_name = ""

        if arcpy.Exists(out_feature_class):
            arcpy.Delete_management(out_feature_class)

        arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class, join_operation, join_type,
                                   field_mapping, match_option, search_radius, distance_field_name)

        # ensure heatmap has been created
        if arcpy.Exists(out_feature_class):
            print(Fore.RED + "Heatmap " + Fore.RESET + "successfully generated for '" + sp + "'.\n-------")


species_list= []

with open(os.path.join(input_directory, data_file)) as spp_csv:
    header_line = next(spp_csv)  # skips first line (column headings)
    try:
        for row in csv.reader(spp_csv):
            if row[0] not in species_list:
                species_list.append(row[0])
    except:
        pass

print("\nThere are " + Fore.BLACK + Back.WHITE + str(len(species_list)) + " species" + Style.RESET_ALL + " in your dataset:")
print(species_list)
print("Each species will be extracted to its own .csv file...")

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
species_file_list = glob.glob("*.csv")

species_heatmap(species_file_list)

arcpy.Delete_management(os.path.join(input_directory, "temporary_files"))
print("\n-------------------------\n-temporary files removed-\n-------------------------\n")

# confirm all heatmaps have been created successfully
print(Fore.GREEN + "*************************************************************************\n" +
      Fore.RESET + "All species heatmaps have been generated and can now be viewed in ArcGIS.\n" +
                   "(Symbology tip: use 'Graduated Colors' and adjust # of classes as needed)\n\n" +
       Fore.CYAN + "~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~\n" +
                   "<'))))><  <']]]]>  <<'}}}}><   - THE END -   ><{{{{'>  ><[[[['>  ><(((('>")

