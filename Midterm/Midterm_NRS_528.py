### Midterm
### Tool
### Challenge

## NRS-528 ##
## K. Corbett

## Giving my best go at script duplicating first third of custom modelbuilder tool built to georeference drone imagery,
## as part of data processing needs for MSc thesis research.

## The first step brings in the .csv file containing pertinent metadata for steps to georeference the input images.
## Then the .csv gets converted to a point feature class (based on lat/longs in the metadata file), which gets projected
## into a UTM coordinate system (metric units helpful for next steps involving calculations with altitude (in meters),
## and camera sensor width and focal length (both in millimeters).

import arcpy

workspace = r"C:\Data\Students_2022\Corbett\Midterm\midterm_data"
arcpy.env.workspace = workspace

# 'XY Table to Point Tool' converts the .csv metadata file to a point feature class
# arcpy.management.XYTableToPoint(in_table, out_feature_class, x_field, y_field, {z_field}, {coordinate_system})

# Setting variables for tool:
in_table = "drone_imagery_metadata.csv"
out_feature_class = "image_cntr_coords"
x_coords = "Longitude"
y_coords = "Latitude"
z_coords = ""
spRef = arcpy.SpatialReference(4326)  # (4326 = GCS_WGS_1984)

# Projecting to UTM coordinate system (26919 = NAD 1983 Zone 19N)
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(26919)

    ### *** not sure why, but for some reason, in this next step below, when the .csv table gets converted to
    ###     to a point feature class, the column headings end up truncated to a 10-character limit in the output...

# Creating XY event layer:
arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords, z_coords, spRef)

    ### *** little unsure if/why this next step is totally necessary... shouldn't the feature class I created work as
    ###     the input to arcpy.AddXY? I tried this first, using 'out_feature_class', but it fails. It works once I use
    ###     arcpy.Copy though... why is this?

# Copying data
in_data = out_feature_class
out_data = "image_cntr_coords_xy.shp"
arcpy.Copy_management(in_data, out_data)

# Adding XY (Easting/Northing) columns to the feature class's ("image_cntr_coords_xy.shp") attribute table:
arcpy.AddXY_management(out_data)

#  Adding five new fields to the new point feature class, including:
#  1) column for calculating each images ground sampling distance (in meters): GSD_m
#  2) column for calculating distances from image's center pixel X value to center left edge pixel: XSHIFT_m
#  3) column for calculating distances from image's center pixel Y values to center upper edge pixel: YSHIFT_m
#  4) two columns, 'ULX' and 'ULY' calculate the new XY coordinates for the upper left pixel of the image,
#     the format needed for georeferencing instructions in a World File

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
                                               field="GSD_m", expression="((" +sensor_width+ "*!Altitude!*100)/"
                                                                          "(" +focal_length+ "*" +image_width+ "))/100",
                                               expression_type="PYTHON3", code_block="", field_type="DOUBLE")


# Calculating the X and Y shifts (in meters) needed to move coordinates from center pixel to upper left pixel
# (needed for World File format)

out_data_XYshifts = arcpy.management.CalculateFields(out_data_GSD, expression_type="PYTHON3",
                                               fields=[["XSHIFT_m", str(int(image_width)/2) + "*!GSD_m!"],
                                                       ["YSHIFT_m", str(int(image_width)/2) + "*!GSD_m!"]],
                                               code_block="")


# Calculating new upper left pixel coordinates using XY shifts from original center pixel XY coordinates

out_data_newXY = arcpy.management.CalculateFields(out_data_XYshifts, expression_type="PYTHON3",
                                                                     fields=[["ULX", "!POINT_X! - !XSHIFT_m!"],
                                                                             ["ULY", "!POINT_Y! + !YSHIFT_m!"]],
                                                                     code_block="")
