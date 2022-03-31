### Midterm Tool Challenge - NRS 528 ###

## Giving a go at producing a script that performs several of the early steps my M.S. project
## modelbuilder tool accomplishes. I'm going to bring in the metadata .csv file containing the
## information pertinent to steps needed for georeferencing images. The .csv will be read in and
## converted to a point feature class (based on lat/longs in the metadata file), which is then projected.
## it to a UTM coordinate system so meters will be used as a unit of measurement. This is necessary
## for following steps, which add fields to the point feature class layer and populates them with
## calculated values needed to ultimately compute each image's Ground Sampling Distance,
## or GSD, which are:
##           altitude of the UAS when the image was captured
##           and some camera parameters: sensor width, focal length, image width and height in pixels
## Sensor width and focal length are provided mm, making a coordinate system in meters beneficial
## when making calculations.

## We will basically be attempting to transpose a photo captured by a drone in the air, that also happened to
## store some other useful info in that photo's digital data we can use to roughly estimate the "real world"
## footprint captured by that image, then place it there for visualization and analysis.

## I'll start by bringing in the metadata .csv file and converting it to point feature class


import arcpy

## I was just messing around trying to make a thing work here... basically allow the user to set the workspace
## but I couldn't figure it out... and there's probably a better way

# pick = input("\nWould you like to use the default workspace (enter D)?"
#             "\nOr, would you like to set a custom workspace (enter C)? ")
#
# if pick == 'D' or 'd':
#     arcpy.env.workspace = r"C:\Users\Kristopher\Documents\NRS528_submissions_REPO\midterm_data"
#     print(r"You are using the default workspace - C:\Users\Kristopher\Documents\NRS528_submissions_REPO\midterm_data")
# elif pick == 'C' or 'c':
#     arcpy.env.workspace = input("Enter the path to your desired workspace: ")
#
# while pick != 'D'or'd'or'C'or'c':
#     pick = input("\nEnter 'D' if you would like to use the default workspace\nor 'C' if you would like to enter a custom workspace: ")
#     if pick == 'D' or 'd':
#         arcpy.env.workspace = r"C:\Users\Kristopher\Documents\NRS528_submissions_REPO\midterm_data"
#         print(r"You are using the default workspace - C:\Users\Kristopher\Documents\NRS528_submissions_REPO\midterm_data")
#     elif pick == 'C' or 'c':
#         arcpy.env.workspace = input("Enter the path to your desired workspace: ")

## other possible first steps to add include: automatically generating a .csv from images using exiftool,
## then giving the user an opportunity to output the column headings in order to see how their various metadata is named

arcpy.env.workspace = r"C:\Users\Kristopher\Documents\NRS528_submissions_REPO\midterm_data"

# user can upload a unique metadata file
input_mdata = input("\nEnter the absolute path to your .csv metadata file: ")

### possibly add step here copying/saving the metadata file into the workspace environment folder

# 'XY Table to Point Tool' converts .csv metadata file to a point feature class
# arcpy.management.XYTableToPoint(in_table, out_feature_class, x_field, y_field, {z_field}, {coordinate_system})

# Setting the local variables for the tool:
in_table = input_mdata
out_feature_class = "image_cntr_coords"
x_coords = "Longitude"
y_coords = "Latitude"
z_coords = ""

# Setting a spatial reference (4326 = GCS_WGS_1984)
spRef = arcpy.SpatialReference(4326)
# Projecting the output to a UTM coordinate system (NAD 1983 Zone 19N = 26919) for units in meters
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(26919)

## Potential to add a step here... instead of assigning the coordinate system, allow the user to input their own desired
## coordinate system. Could even ask if they'd like to see a list of common useful coordinate systems and their codes.

# Creating the XY event layer:

### *** for some reason, right here, when the .csv table gets converted to a point feature class, the column/field
###     headings get truncated to 10 characters. No idea why.
arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords, z_coords, spRef)

# Copying data to preserve original dataset
# I'm a little unsure why this is necessary... doesn't the point feature class I just created suffice?
# However, I've tried running without using arcpy.Copy and it fails to execute arcpy.AddXY ...why?
in_data = "image_cntr_coords.shp"
out_data = "image_cntr_coords_xy.shp"
arcpy.Copy_management(in_data, out_data)

# Adding XY (Easting/Northing) columns to the feature class's ("image_cntr_coords_xy.shp") attribute table:
arcpy.AddXY_management(out_data)

#  Adding five new fields to the new point feature class, including:
#  1) column to calculate/populate ground sampling distances (in meters): GSD_m
#  2) column to calculate/populate distances from center pixel X value to image left edge: XSHIFT_m
#  3) column to calculate distances from center pixel Y value to image upper edge: YSHIFT_m
#  4) two columns, 'ULX' and 'ULY' to contain new XY coordinates, now at the upper left corner pixel of the image
#     new coordinates will be used as georeferencing instructions in a World File

out_data_add_fields = arcpy.management.AddFields(out_data, [["GSD_m", "DOUBLE", "", "", "", ""],
                                                            ["XSHIFT_m", "DOUBLE", "", "", "", ""],
                                                            ["YSHIFT_m", "DOUBLE", "", "", "", ""],
                                                            ["ULX", "DOUBLE", "", "", "", ""],
                                                            ["ULY", "DOUBLE", "", "", "", ""]])

# Populating the GSD_m column with calculated ground sampling distances; with user able to
# specify values for altitude and camera specs (sensor width, focal length, image width)
# arcpy.management.CalculateField(in_table, field, expression, {expression_type}, {code_block}, {field_type}, {enforce_domains})?

sensor_width = input("camera sensor width in mm: ")
focal_length = input("camera focal length in mm: ")
image_width = input("number of horizontal pixels in image: ")
image_height = input("number of vertical pixels in image: ")

out_data_GSD = arcpy.management.CalculateField(in_table=out_data_add_fields,
                                               field="GSD_m",
                                               expression="((" +sensor_width+ "*!Altitude!*100)/"
                                                           "(" +focal_length+ "*" +image_width+ "))/100",
                                               expression_type="PYTHON3",
                                               code_block="",
                                               field_type="DOUBLE")

# Calculating the X and Y shifts (in meters) needed to move coordinates from center pixel to upper left pixel (World File format)

out_data_XYshifts = arcpy.management.CalculateFields(out_data_GSD, expression_type="PYTHON3",
                                               fields=[["XSHIFT_m", str(int(image_width)/2) + "*!GSD_m!"],
                                                       ["YSHIFT_m", str(int(image_width)/2) + "*!GSD_m!"]],
                                               code_block="")

# Performing coordinate shift calculations

out_data_newXY = arcpy.management.CalculateFields(out_data_XYshifts, expression_type="PYTHON3",
                                                                     fields=[["ULX", "!POINT_X! - !XSHIFT_m!"],
                                                                             ["ULY", "!POINT_Y! + !YSHIFT_m!"]],
                                                                     code_block="")
