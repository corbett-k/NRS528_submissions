# Coding Challenge 4: Choose and Use a Tool in arcpy

# My aim is to take a .csv file containing metadata extracted from drone-captured images and perform some
# preliminary steps that will eventually allow me to properly import and manipulate the source images in ArcGIS Pro

# The first step will be to access the .csv metadata file and convert its contents to a point feature class...
# To accomplish this, I will use the 'XY Table To Point' tool within arcpy:

import arcpy

# Set environment settings:
arcpy.env.workspace = r"G:\My Drive\Coursework\Spring 2022 Courses\NRS 528\Coding Challenges\Challenge 4\GIS_datafiles"

# From the ArcGIS Pro online help documentation for the 'XY Table to Point Tool':
# arcpy.management.XYTableToPoint(in_table, out_feature_class, x_field, y_field, {z_field}, {coordinate_system})

# Setting the local variables:
in_table = r"drone_imagery_metadata.csv"
out_feature_class = "image_center_points"
x_coords = "GPSLongitude"
y_coords = "GPSLatitude"
z_coords = ""

# Setting the spatial reference (as GCS_WGS_1984):
spRef = arcpy.SpatialReference(4326)
# Setting the output spatial reference to a projected coordinate system, in this case NAD 1983 UTM Zone 19N
# This will allow me to then use the 'Add XY' geoprocessing tool to output Easting/Northing values in meters...
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(26919)

# Making the XY event layer:
arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords, z_coords, spRef)

# Next, I'd like to convert the lat/long coordinates to Easting/Northing format (essential for subsequent steps...)
# syntax from online tool documentation : arcpy.management.AddXY(in_features)

# Setting local variables:
in_data = "image_center_points.shp"
in_features = "image_center_points_XY.shp"

# Copying data to preserve original dataset:
arcpy.Copy_management(in_data, in_features)

# Execute AddXY
arcpy.AddXY_management(in_features)
