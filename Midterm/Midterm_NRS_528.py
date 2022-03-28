        ### Midterm Tool Challenge - NRS 528 ###

    ## Giving a go at producing a script that performs several of the early steps my M.S. project
    ## modelbuilder tool accomplishes. I'm going to bring in the metadata .csv file containing the
    ## information pertinent to steps needed for georeferencing images. The .csv will be read in and
    ## converted to a point feature class (based on lat/longs in the metadata file), which is then projected.
    ## it to a UTM coordinate system so meters will be used as a unit of measurement. This is necessary
    ## for following steps, which add fields to the point feature class layer and populates them with
    ## calculated values needed to ultimately compute each image's Ground Sampling Distance,
    ## or GSD, which are:
        # altitude of the UAS when the image was captured
        # and some camera parameters: sensor width, focal length, image width and height in pixels
    ## Sensor width and focal length are provided mm, making a coordinate system in meters beneficial
    ## when making calculations.

    ## We will basically be attempting to transpose a photo captured by a drone in the air, that also happened to
    ## store some other useful info in that photo's digital data we can use to roughly estimate the "real world"
    ## footprint captured by that image, then place it there for visualization and analysis.

    ## I'll start by bringing in the metadata .csv file and converting it to point feature class


import arcpy

arcpy.env.workspace = r"C:\Users\Kristopher\Documents\NRS528_submissions_REPO\midterm_data"  # setting my workspace environment

input_mdata = input("Paste the absolute path to the folder containing your metadata (.csv) file: \n  Here>>  ")

    ## I'll first use the 'XY Table to Point Tool' to to access the .csv metadata file and convert its contents to a point feature class
    ## arcpy.management.XYTableToPoint(in_table, out_feature_class, x_field, y_field, {z_field}, {coordinate_system})

# Setting my local variables:
in_table = input_mdata
out_feature_class = "image_centers"
x_coords = "GPSLongitude"
y_coords = "GPSLatitude"
z_coords = ""

# Setting a spatial reference (as GCS_WGS_1984):
# spRef = arcpy.SpatialReference(4326)
spRef = arcpy.SpatialReference(26919)

# # Projecting the output to a UTM coordinate system (NAD 1983 Zone 19N) for units in meters
# arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(26919)

# Creating the XY event layer:
arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords, z_coords, spRef)

# Adding Easting(X)/Northing(Y) coordinate columns to the point feature class attributes table
arcpy.AddXY_management(out_feature_class)

# Adding fields to the point feature class 'image_centers', including:
    # 1) a column in which to calculate ground sampling distance (in meters); GSD_m
    # 2) a column for determining the distance from the center pixel X coordinate to the left edge; XSHIFT_m
    #    shift distance = GSD (i.e., size of pixel, in m) X 1/2 sensor width in # of pixels
    # 3) a column for determining the distance from the center pixel Y coordinate to the upper edge; YSHIFT_m
    #    shift distance = GSD X 1/2 sensor height in # of pixels
    # 4) two columns, 'ULX' and 'ULY' that will contain the new XY coordinates to be used as the upper left
    #    pixel coordinate that will populate the georeferencing instructions of my to be created World File
    #    (i.e., original X - shift, original Y - shift)

arcpy.management.AddFields(out_feature_class, ["GSD_m", "DOUBLE", "", "", "", ""],
                                              ["XSHIFT_m", "DOUBLE", "", "", "", ""],
                                              ["YSHIFT_m", "DOUBLE", "", "", "", ""],
                                              ["ULX", "DOUBLE", "", "", "", ""],
                                              ["ULY", "DOUBLE", "", "", "", ""])

# Calculating the Ground Sanpling Distance column values, using operator specified values for altitude and camera specs
arcpy.management.CalculateField(in_table=out_feature_class, field="GSD_m", expression="((35.9*!RelativeAltitude!*100)/(35*8192))/100",
                                        expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")

# Calculating the X and Y shift values needed to move coordinates from center to upper left corner for World File

arcpy.management.CalculateFields(out_feature_class, expression_type="PYTHON3", fields=[["XSHIFT_m", "4096*!GSD_m!"],
                                ["YSHIFT_m", "2730*!GSD_m!"]], code_block="", enforce_domains="NO_ENFORCE_DOMAINS")

# Performing coordinate shift calculations

arcpy.management.CalculateFields(out_feature_class, expression_type="PYTHON3", fields=[["ULX", "!POINT_X! - !XSHIFT_m!"],
                                ["ULY", "!POINT_Y! + !YSHIFT_m!"]], code_block="", enforce_domains="NO_ENFORCE_DOMAINS")


