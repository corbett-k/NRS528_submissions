
import arcpy
import os
# from colorama import Fore

work_dir = r'C:\Users\krist\Documents\GitHub\NRS528_submissions\Final_Challenge'
arcpy.env.workspace = work_dir


if not os.path.exists(os.path.join(work_dir, 'rotated_rasters.gdb')):
    # arcpy.management.CreateFileGDB(out_folder_path, out_name, {out_version})
    arcpy.CreateFileGDB_management(out_folder_path=work_dir, out_name='rotated_rasters.gdb')

fileGDB = os.path.join(work_dir, 'rotated_rasters.gdb')

images_dir = os.path.join(work_dir, r'input_data\test_images')
output_dir = os.path.join(work_dir, 'output_files')

input_shp = os.path.join(output_dir, 'image_coords_xy.shp')
fields = ['FileName', 'GSD_m', 'ULX', 'ULY', 'GimbalYaw']

with arcpy.da.SearchCursor(input_shp, fields) as cursor:

    for row in cursor:

        jpg_filename = row[0]
        GSD = row[1]
        worldFile_X = row[2]
        worldFile_Y = row[3]
        rotation = row[4]

        txt_file = os.path.join(images_dir, jpg_filename.replace('.JPG', '.txt'))

        # create text file containing world file georeferencing instructions:
        with open(txt_file, 'w') as new_txt_file:
            new_txt_file.write(str(GSD) + '\n0\n0\n' + '-' + str(GSD) + '\n' + str(worldFile_X) + '\n' + str(worldFile_Y))

        filename_no_ext = os.path.splitext(txt_file)[0]
        os.rename(txt_file, filename_no_ext + '.jgw')

        # arcpy.conversion.RasterToGeodatabase(Input_Rasters, Output_Geodatabase, {Configuration_Keyword})
        image_in = os.path.join(images_dir, jpg_filename)
        arcpy.RasterToGeodatabase_conversion(Input_Rasters=image_in, Output_Geodatabase=fileGDB)

        GDB_raster_in = os.path.join(fileGDB, filename_no_ext)
        print(GDB_raster_in)

        # if arcpy.Exists(GDB_raster_in):
        #     print(Fore.GREEN + "Image: " + Fore.RESET + jpg_filename + Fore.GREEN + " successfully loaded to geodatabase..." + Fore.RESET)
        #
        # rotate_raster = GDB_raster_in + '_r'
        #
        # # arcpy.management.Rotate(in_raster, out_raster, angle, {pivot_point}, {resampling_type}, {clipping_extent})
        # arcpy.Rotate_management(in_raster=GDB_raster_in, out_raster=GDB_raster_in, angle=rotation)
