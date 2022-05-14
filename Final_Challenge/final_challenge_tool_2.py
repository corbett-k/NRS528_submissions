
import arcpy
import os

work_dir = r'C:\Users\krist\Documents\GitHub\NRS528_submissions\Final_Challenge'
arcpy.env.workspace = work_dir

input_dir = os.path.join(work_dir, 'input_data')
images_dir = os.path.join(input_dir, 'test_images')
output_dir = os.path.join(work_dir, 'output_files')

txt_files_dir = os.path.join(output_dir, 'txt_files')
if not os.path.exists(txt_files_dir):
    os.mkdir(txt_files_dir)

input_shp = os.path.join(output_dir, 'image_coords_xy.shp')
fields = ['FileName', 'ULX', 'ULY', 'GimbalYaw']

with arcpy.da.SearchCursor(input_shp, fields) as cursor:

    for row in cursor:

        filename = row[0]
        worldFile_X = row[1]
        worldFile_Y = row[2]
        rotation = row[3]

        filename_no_ext = filename.rstrip('.JPG')
        txt_file = filename_no_ext + '.txt'
        jgw_file = filename_no_ext + '.jgw'

        # arcpy.env.workspace = txt_files_dir
        # creating .txt file shell (becomes image's world file; txt extension modified to .jgw)
        # arcpy.conversion.TableToTable(in_rows, out_path, out_name, {where_clause}, {field_mapping}, {config_keyword})

        arcpy.conversion.TableToTable(in_rows=row, out_path=txt_files_dir, out_name=txt_file,
                                      field_mapping="GSD_m \"GSD_m\" true true false 8 Double 0 0,First,"
                                                    "#,I_image_metadata_XYTableToPoint_FileName,GSD_m,-1,-1;ULX \"ULX\" "
                                                    "true true false 8 Double 0 0,First,#,I_image_metadata_XYTableToPoint_FileName,"
                                                    "ULX,-1,-1;ULY \"ULY\" true true false 8 Double 0 0,First,#,"
                                                    "I_image_metadata_XYTableToPoint_FileName,ULY,-1,-1")

        read_txt_file = open(txt_file, 'r')  # open txt file in read mode
        line = read_txt_file.readlines()[1]  # get all lines from txt file but only keep 2nd line (which has all the data)
        read_txt_file.close()  # close input file

        inValues = line.split(",")  # split <line> to extract individual values
        outValues = [inValues[1], "0", "0", "-" + inValues[1], inValues[2], inValues[3]]  # create list of output values

        world_file = os.path.join(images_dir, file + '.jgw')

        write_world_file = open(world_file, "w")  # create and open output file
        for val in outValues:  # for each value...
            write_world_file.write("%s\n" % val)  # write value to output file
        write_world_file.close()  # close output file

        # arcpy.management.CopyRaster(in_raster, out_rasterdataset, {config_keyword}, {background_value}, {nodata_value},
        # {onebit_to_eightbit}, {colormap_to_RGB}, {pixel_type}, {scale_pixel_value}, {RGB_to_Colormap}, {format},
        # {transform}, {process_as_multidimensional}, {build_multidimensional_transpose})

        arcpy.management.CopyRaster(in_raster=filename, out_rasterdataset=name)
