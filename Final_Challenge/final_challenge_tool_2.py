#### NRS-528 #######################
#### Semester Final Coding Challenge
############################ Tool #2

import arcpy
import os
# from colorama import Fore

### DEFINE WORKSPACE
work_dir = r'C:\Users\krist\Documents\GitHub\NRS528_submissions\Final_Challenge'
arcpy.env.workspace = work_dir

### ALLOW OVERWRITING OF ARCGIS PRO OUTPUTS
arcpy.env.overwriteOutput = True

### CREATE FILE GEODATABASE, INTO WHICH JPEG IMAGES WILL BE ADDED (AS ESRI GRID FORMAT; ** parameterize later)
fileGDB = os.path.join(work_dir, 'DGtool_Outputs.gdb')
if os.path.exists(fileGDB):
    print("\n'DGtool_Outputs.gdb' exists in workspace directory (rotated rasters and mosaic dataset output location) ...")
else:
    arcpy.CreateFileGDB_management(out_folder_path=work_dir, out_name='DGtool_Outputs.gdb')
    # arcpy.management.CreateFileGDB(out_folder_path, out_name, {out_version})
    print("\nNew geodatabase 'DGtool_Outputs.gdb' created in current workspace directory ...")

### DEFINE DIRECTORY PATH TO IMAGES
images_dir = os.path.join(work_dir, r'input_data\test_images')

### DEFINE DIRECTORY PATH TO SHAPEFILE AND ATTRIBUTE TABLE FIELDS TO BE USED
input_shp = os.path.join(work_dir, r'output_files\image_coords_xy.shp')
fields = ['FileName', 'GSD_m', 'ULX', 'ULY', 'GimbalYaw']

### DEFINE SPATIAL REFERENCE FOR GEOPROCESSING TASKS
spRef = arcpy.SpatialReference(26919)  # 26919 = NAD 1983 Zone 19N; UTMs required for WF format correspondence

def Rotate(inRaster, outRaster, angle):
    arcpy.Rotate_management(inRaster, outRaster, angle)
    return outRaster

### PROCESSING METADATA: WORLD FILE GEOREFERENCING AND RASTER ROTATION
### LOOP THROUGH ROWS OF SHAPEFILE ATTRIBUTE TABLE USING SEARCH CURSOR
with arcpy.da.SearchCursor(input_shp, fields) as cursor:

    for row in cursor:

        jpg_file = str(row[0])
        GSD = row[1]
        WorldFile_X = row[2]
        WorldFile_Y = row[3]
        raster_rotation = row[4]

        ### DEFINE TEXT/WORLD FILE NAME AND OUTPUT LOCATION
        txt_file = os.path.join(images_dir, jpg_file.replace('JPG', 'txt'))
        world_file = os.path.join(images_dir, jpg_file.replace('JPG', 'jgw'))

        ### CREATE TEXT FILE ...
        if not os.path.exists(txt_file) and not os.path.exists(world_file):
            write_txt_file = open(txt_file, 'w')
            write_txt_file.write(str(GSD) +
                                 '\n0\n0' +
                                 '\n-' + str(GSD) +
                                 '\n' + str(WorldFile_X) +
                                 '\n' + str(WorldFile_Y))
            write_txt_file.close()

            ### ... AND CONVERT TO WORLD FILE (.txt TO .jgw for JPEG rasters; ** parameterize later)
            os.rename(txt_file, txt_file.replace('txt', 'jgw'))

        if os.path.exists(txt_file):
            if not os.path.exists(world_file):
                os.rename(txt_file, txt_file.replace('txt', 'jgw'))

        ### COPY RASTER TO GDB
        ### i.e., move world file georeferenced jpeg images to geodatabase (as esri grid format)
        jpg_path = os.path.join(images_dir, jpg_file)
        GDB_raster = jpg_file.replace('.JPG', '')
        GDB_raster_path = os.path.join(fileGDB, GDB_raster)

        with arcpy.EnvManager(outputCoordinateSystem=spRef):
            arcpy.CopyRaster_management(in_raster=jpg_path, out_rasterdataset=GDB_raster_path,
                                        nodata_value="256", format="JPEG", transform="Transform")
        # arcpy.management.CopyRaster(in_raster, out_rasterdataset, {config_keyword}, {background_value},
        # {nodata_value}, {onebit_to_eightbit}, {colormap_to_RGB}, {pixel_type}, {scale_pixel_value},
        # {RGB_to_Colormap}, {format}, {transform}, {process_as_multidimensional}, {build_multidimensional_transpose})

        if arcpy.Exists(GDB_raster_path):
            print("Image " + jpg_file + " moved to geodatabase...")

        # ### ROTATE RASTER
        # rotated_GDB_raster = GDB_raster + '_r'
        # arcpy.Rotate_management(in_raster=GDB_raster, out_raster=rotated_GDB_raster, angle=raster_rotation)
        # # arcpy.management.Rotate(in_raster, out_raster, angle, {pivot_point}, {resampling_type}, {clipping_extent})

        rotated_GDB_raster = GDB_raster + '_r'
        rotated_GDB_raster_path = os.path.join(fileGDB, rotated_GDB_raster)

        Rotate(GDB_raster_path, GDB_raster_path + '_r', raster_rotation)

        if arcpy.Exists(GDB_raster_path):
            print("Raster " + GDB_raster + " rotated...\n")

print("All rasters georeferenced. Run Tool #3 for mosaicking process ...")
