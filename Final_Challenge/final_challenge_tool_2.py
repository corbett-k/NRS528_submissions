
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
fields = ['FileName', 'GSD_m', 'ULX', 'ULY', 'GimbalYaw']

with arcpy.da.SearchCursor(input_shp, fields) as cursor:

    for row in cursor:

        filename = row[0]
        GSD = row[1]
        worldFile_X = row[2]
        worldFile_Y = row[3]
        rotation = row[4]

        txt_file = os.path.join(txt_files_dir, (filename).replace('.JPG', '.txt'))

        # create text file containing world file georeferencing instructions:
        with open(txt_file, 'w') as new_txt_file:
            new_txt_file.write(str(GSD) + '\n0\n0\n' + '-' + str(GSD) + '\n' + str(worldFile_X) + '\n' + str(worldFile_Y))

        base = os.path.splitext(txt_file)[0]
        os.rename(txt_file, base + '.jgw')
