#### NRS-528 #######################
#### Semester Final Coding Challenge
############################ Tool #1

# import os
import sys
import arcpy
from colorama import Fore

### DEFINE WORKSPACE
# arcpy.env.workspace = work_dir

### ALLOW OVERWRITING OF ARCGIS PRO OUTPUTS
arcpy.env.overwriteOutput = True

### DEFINE DIRECTORY PATH TO .CSV INPUT (METADATA IN TABLE FILE FORMAT)
input_csv = sys.argv[1]  # os.path.join(work_dir, 'input_data')  # XYTableToPoint accepts table view at data type
# images_dir = os.path.join(input_dir, 'test_images')
# input_csv = os.path.join(input_dir, 'image_metadata.csv')

### DEFINE SAVE LOCATION AND NAME OF OUTPUT POINT FEATURE CLASS (SHAPEFILE)
# output_shp = sys.argv[2]  # os.path.join(work_dir, 'output_files')
# if not os.path.exists(output_dir):
#     os.mkdir(output_dir)

### DETERMINE CATEGORIES OF METADATA AVAILABLE IN .CSV TABLE FILE
fields_list = [f.name for f in arcpy.ListFields(input_csv)]
row_count = arcpy.GetCount_management(input_csv)

### PROVIDE USER WITH METADATA CATEGORIES AND NUMBER OR IMAGES REPRESENTED IN TABLE FILE
print("\n" + Fore.GREEN + "Categories (columns) of metadata extracted: " + Fore.RESET + str(len(fields_list)) +
      "\n" + str((sorted(fields_list))).replace("[", "").replace("]", "").replace("'", "").lower() + Fore.GREEN +
      "\n\nNumber of images (rows) represented in metadata: " + Fore.RESET + str(row_count))


### CONVERT TABLE FILE (USING EMBEDDED GPS COORDINATES) TO A POINT VECTOR DATASET WITH METADATA PRESENRVED AS ATTRIBUTES
output_lyr = "temp_layer.shp"
x_coords = "Longitude"
y_coords = "Latitude"

spRef = arcpy.SpatialReference(4326)  # (4326 = GCS_WGS_1984)
PrjCS = arcpy.SpatialReference(26919)  # (26919 = NAD 1983 Zone 19N)

with arcpy.EnvManager(outputCoordinateSystem=PrjCS):  # output to projected coordinate system
  # arcpy.XYTableToPoint_management(in_table, out_feature_class, x_field, y_field, {z_field}, {coordinate_system})
    arcpy.XYTableToPoint_management(in_table=input_csv, out_feature_class=output_lyr,
                                    x_coords=x_coords, y_coords=y_coords, spRef=spRef)
    # arcpy.XYTableToPoint_management(in_table, out_feature_class, x_field, y_field, {z_field}, {coordinate_system})

### STORE COPY TO OUTPUT DIRECTORY

arcpy.Copy_management(output_lyr,sys.argv[2])

### PRINT STATEMENT CONFIRMING SUCCESSFUL CONVERSION OF METADATA .CSV TABLE FILE TO SHAPEFILE (POINT FEATURE CLASS)
if arcpy.Exists(output_shp):
    # print("\n" + Fore.GREEN + ".csv table file converted to shapefile: " + Fore.RESET + "image_coord_xy.shp")
    print(".csv table file converted to shapefile ...")

### ADD XY (EASTING/NORTHING) COLUMNS TO FEATURE CLASS ATTRIBUTE TABLE:
arcpy.AddXY_management(output_shp)

### ADD 5 NEW FIELDS TO POINT FEATURE CLASS ATTRIBUTE TABLE:
#   1) column to calculate each images ground sampling distance (in meters): GSD_m
#   2) column to calculate distances from image's center pixel X value to center left edge pixel: XSHIFT_m
#   3) column to calculate distances from image's center pixel Y values to center upper edge pixel: YSHIFT_m
#   4) column to calculate upper left corner pixel coordinate: ULX
#   5) column to calculate upper left corner pixel coordinate: ULY

added_fields = arcpy.AddFields_management(output_shp, [["GSD_m", "DOUBLE", "", "", "", ""],
                                                       ["XSHIFT_m", "DOUBLE", "", "", "", ""],
                                                       ["YSHIFT_m", "DOUBLE", "", "", "", ""],
                                                       ["ULX", "DOUBLE", "", "", "", ""],
                                                       ["ULY", "DOUBLE", "", "", "", ""]])
if arcpy.Exists(added_fields):
    # print(Fore.GREEN + "\nNew fields added to shapefile attribute table ..." + Fore.RESET)
    print("New fields added to shapefile attribute table ...")

### FIELD CALCULATIONS USING CALCULATE FIELD(S)
# arcpy.management.CalculateField(in_table, field, expression, {expression_type}, {code_block}, {field_type})
# arcpy.management.CalculateFields(in_table, expression_type, fields, {code_block}, {enforce_domains})

### POPULATE 'GSD_m' COLUMN WITH CALCULATED GROUND SAMPLING DISTANCE VALUES

cam_sys = sys.argv[3]
if cam_sys == 'DJI Zenmuse H20T':
    sensor_width = '6.5625'
    focal_length = '4.5'
    image_width = '4056'
    image_height = '3040'
elif cam_sys == 'DJI Zenmuse P1':
    sensor_width = '35.9'
    focal_length = '35'
    image_width = '8192'
    image_height = '5460'

calculate_GSD = arcpy.CalculateField_management(in_table=added_fields, field="GSD_m", expression="((" + sensor_width +
                                                "*!Altitude!*100)/(" + focal_length + "*" + image_width + "))/100",
                                                expression_type="PYTHON3", field_type="DOUBLE")
if arcpy.Exists(calculate_GSD):
    print(Fore.GREEN + "Attribute table populated with ground sampling distance values ..." + Fore.RESET)

### CALCULATE XY SHIFTS TO MOVE COORDINATES FROM CENTER TO UPPER LEFT PIXEL (WORLD FILE FORMAT)
XYshifts = arcpy.CalculateFields_management(in_table=calculate_GSD, expression_type="PYTHON3",
                                            fields=[["XSHIFT_m", str(int(image_width)/2) + "*!GSD_m!"],
                                                    ["YSHIFT_m", str(int(image_height)/2) + "*!GSD_m!"]])

if arcpy.Exists(XYshifts):
    print(Fore.GREEN + "Attribute table populated with X and Y shift values ..." + Fore.RESET)

# CALCULATE NEW UPPER LEFT PIXEL COORDINATES USING XY SHIFT VALUES
newXYcoords = arcpy.CalculateFields_management(in_table=XYshifts, expression_type="PYTHON3",
                                               fields=[["ULX", "!POINT_X! - !XSHIFT_m!"],
                                                       ["ULY", "!POINT_Y! + !YSHIFT_m!"]])
if arcpy.Exists(newXYcoords):
    print(Fore.GREEN + "Attribute table populated with new XY coordinates ..." + Fore.RESET)

print(Fore.CYAN + "\nShapefile " + Fore.RESET + "image_coords_xy.shp" + Fore.CYAN + " attribute table successfully "
      "populated with all values needed for georeferencing images in Tool #2." + Fore.RESET)
