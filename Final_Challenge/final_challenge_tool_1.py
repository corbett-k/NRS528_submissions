
import arcpy
import os
from colorama import Fore

work_dir = r'C:\Users\krist\Documents\GitHub\NRS528_submissions\Final_Challenge'
arcpy.env.workspace = work_dir

input_dir = os.path.join(work_dir, 'input_data')
images_dir = os.path.join(input_dir, 'test_images')
input_csv = os.path.join(input_dir, 'image_metadata.csv')

fields_list = [f.name for f in arcpy.ListFields(input_csv)]
row_count = arcpy.GetCount_management(input_csv)

print("\n"+ str(len(fields_list)) + Fore.BLUE + " categories of metadata extracted:\n    "+ Fore.RESET +
      str((sorted(fields_list))).replace("[", "").replace("]", "").replace("'", "").lower() + Fore.BLUE +
      "\n\nNumber of rows / images represented in metadata : " + Fore.RESET + str(row_count))

# 'XY Table to Point Tool' converts the .csv metadata file to a point feature class
# arcpy.management.XYTableToPoint(in_table, out_feature_class, x_field, y_field, {z_field}, {coordinate_system})

in_table = input_csv
out_feature_class = "image_coords.shp"
x_coords = "Longitude"
y_coords = "Latitude"
z_coords = ""
spRef = arcpy.SpatialReference(4326)  # (4326 = GCS_WGS_1984)

# Projecting to UTM coordinate system (26919 = NAD 1983 Zone 19N)
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(26919)

output_dir = os.path.join(work_dir, 'output_files')
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

arcpy.env.workspace = output_dir

# Creating XY event layer:
layer = arcpy.XYTableToPoint_management(in_table, out_feature_class, x_coords, y_coords, z_coords, spRef)

pt_shp = "image_coords_xy.shp"
arcpy.Copy_management(layer, pt_shp)

if arcpy.Exists(pt_shp):
    print("\n" + Fore.GREEN + ".csv table file converted to shapefile 'image_coord_xy.shp'" + Fore.RESET)

# Adding XY columns to the feature class attribute table:
arcpy.AddXY_management(pt_shp)

#  Adding five new fields to the new point feature class, including:
#  1) column for calculating each images ground sampling distance (in meters): GSD_m
#  2) column for calculating distances from image's center pixel X value to center left edge pixel: XSHIFT_m
#  3) column for calculating distances from image's center pixel Y values to center upper edge pixel: YSHIFT_m
#  4) two columns, 'ULX' and 'ULY' calculate the new XY coordinates for the upper left pixel of the image,
#     the format needed for georeferencing instructions in a World File

added_fields = arcpy.AddFields_management(pt_shp, [["GSD_m", "DOUBLE", "", "", "", ""],
                                                   ["XSHIFT_m", "DOUBLE", "", "", "", ""],
                                                   ["YSHIFT_m", "DOUBLE", "", "", "", ""],
                                                   ["ULX", "DOUBLE", "", "", "", ""],
                                                   ["ULY", "DOUBLE", "", "", "", ""]])

# Populating the GSD_m column with calculated ground sampling distances; with user able to specify values for altitude
# and camera specs (sensor width, focal length, image width)

# arcpy.management.CalculateField(in_table, field, expression, {expression_type}, {code_block}, {field_type})

sensor_width = '6.5625'
focal_length = '4.5'
image_width = '4056'
image_height = '3040'

calculate_GSD = arcpy.CalculateField_management(in_table=added_fields, field="GSD_m",
                                               expression="((" + sensor_width + "*!Altitude!*100)/(" + focal_length +
                                                          "*" + image_width + "))/100", expression_type="PYTHON3",
                                               code_block="", field_type="DOUBLE")
if arcpy.Exists(calculate_GSD):
    print(Fore.GREEN + "\nShapefile's attribute table populated with ground sampling distance values..." + Fore.RESET)

# Calculating XY shifts (in meters) needed to transfer coordinates from center to upper left pixel (World File format)
XYshifts = arcpy.CalculateFields_management(in_table=calculate_GSD, expression_type="PYTHON3",
                                                     fields=[["XSHIFT_m", str(int(image_width)/2) + "*!GSD_m!"],
                                                             ["YSHIFT_m", str(int(image_height)/2) + "*!GSD_m!"]],
                                                     code_block="")
if arcpy.Exists(XYshifts):
    print(Fore.GREEN + "\nX and Y shift values generated..." + Fore.RESET)

# Calculating new upper left pixel coordinates using XY shift values
newXYcoords = arcpy.CalculateFields_management(in_table=XYshifts, expression_type="PYTHON3",
                                               fields=[["ULX", "!POINT_X! - !XSHIFT_m!"], ["ULY", "!POINT_Y! + !YSHIFT_m!"]],
                                               code_block="")
if arcpy.Exists(newXYcoords):
    print(Fore.GREEN + "\nNew X and Y coordinates generated..." + Fore.RESET)
