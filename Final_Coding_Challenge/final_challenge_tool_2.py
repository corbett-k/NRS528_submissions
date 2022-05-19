#### NRS-528 #######################
#### Semester Final Coding Challenge
############################ Tool #2

import os
import sys
import arcpy
from colorama import Fore

### DEFINE WORKSPACE
arcpy.env.workspace = work_dir = sys.argv[1]

### ALLOW OVERWRITING OF ARCGIS PRO OUTPUTS
arcpy.env.overwriteOutput = True

### CREATE FILE GEODATABASE, INTO WHICH JPEG IMAGES WILL BE ADDED (AS ESRI GRID FORMAT; ** parameterize later)
fileGDB = sys.argv[1]  # os.path.join(work_dir, 'DGtool_Outputs.gdb')

# print(Fore.GREEN + "Creating geodatabase " + Fore.RESET + "DGtool_Outputs.gdb" +
#       Fore.GREEN + " for processing outputs ..." + Fore.RESET)
#
# if os.path.exists(fileGDB):
#     print("\nDGtool_Outputs.gdb" + Fore.GREEN + " already exists in workspace directory ...\n" + Fore.RESET)
# else:
#     arcpy.CreateFileGDB_management(out_folder_path=work_dir, out_name='DGtool_Outputs.gdb')
#     # arcpy.management.CreateFileGDB(out_folder_path, out_name, {out_version})
#     print(Fore.GREEN + "\nNew geodatabase " + Fore.RESET + "DGtool_Outputs.gdb" + Fore.GREEN +
#           " created in current workspace directory ..." + Fore.RESET + "\n")

### DEFINE DIRECTORY PATH TO IMAGES
images_dir = sys.argv[2]  # os.path.join(work_dir, r'input_data\test_images')

### DEFINE DIRECTORY PATH TO SHAPEFILE AND ATTRIBUTE TABLE FIELDS TO BE USED
input_shp = sys.argv[3]  # os.path.join(work_dir, r'output_files\image_coords_xy.shp')
fields = ['FileName', 'GSD_m', 'ULX', 'ULY', 'GimbalYaw']

### DEFINE SPATIAL REFERENCE FOR GEOPROCESSING TASKS
spRef = arcpy.SpatialReference(26919)  # 26919 = NAD 1983 Zone 19N; UTMs required for WF format correspondence

def Rotate(inRaster, outRaster, angle):
    # arcpy.management.Rotate(in_raster, out_raster, angle, {pivot_point}, {resampling_type}, {clipping_extent})
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
        GDB_raster_name = jpg_file.replace('.JPG', '')
        GDB_raster_path = os.path.join(fileGDB, GDB_raster_name)

        with arcpy.EnvManager(outputCoordinateSystem=spRef):
            arcpy.CopyRaster_management(in_raster=jpg_path, out_rasterdataset=GDB_raster_path,
                                        nodata_value="256", format="JPEG", transform="Transform")
        # arcpy.management.CopyRaster(in_raster, out_rasterdataset, {config_keyword}, {background_value}, {nodata_value},
        #       {onebit_to_eightbit}, {colormap_to_RGB}, {pixel_type}, {scale_pixel_value}, {RGB_to_Colormap}, {format},
        #       {transform}, {process_as_multidimensional}, {build_multidimensional_transpose})

        if arcpy.Exists(GDB_raster_path):
            print(Fore.GREEN + "Image " + Fore.RESET + jpg_file + Fore.GREEN + " copied to geodatabase ..." + Fore.RESET)

        # ### ROTATE RASTER
        rotated_GDB_raster_name = GDB_raster_name + '_r'
        rotated_GDB_raster_path = os.path.join(fileGDB, rotated_GDB_raster_name)

        Rotate(GDB_raster_path, rotated_GDB_raster_path, raster_rotation)

        if arcpy.Exists(rotated_GDB_raster_path):
            print(Fore.GREEN + "Raster " + Fore.RESET + GDB_raster_name + Fore.GREEN + " rotated, output as " +
                  Fore.RESET + rotated_GDB_raster_name + Fore.GREEN + " ..." + Fore.RESET)

            arcpy.Delete_management(GDB_raster_path)

        if not arcpy.Exists(GDB_raster_path):
            print(Fore.GREEN + "Intermediate unrotated raster removed from geodatabase ...\n" + Fore.RESET)

print(Fore.CYAN + "Tool processing complete. Georeferenced rasters now ready for mosaicking in Tool #3." + Fore.RESET)
