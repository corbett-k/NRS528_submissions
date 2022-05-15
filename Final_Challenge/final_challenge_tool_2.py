
import arcpy
import os
# from colorama import Fore

### DEFINING THE WORKSPACE
work_dir = r'C:\Users\krist\Documents\GitHub\NRS528_submissions\Final_Challenge'
arcpy.env.workspace = work_dir

### ALLOW OVERWRITING OF OUTPUTS
arcpy.env.overwriteOutput = True

### CREATING A FILE GEODATABASE, INTO WHICH JPEG IMAGES WILL BE ADDED (IN ESRI GRID FORMAT)
fileGDB = os.path.join(work_dir, 'rotated_rasters.gdb')
if not os.path.exists(fileGDB):
    # arcpy.management.CreateFileGDB(out_folder_path, out_name, {out_version})
    arcpy.CreateFileGDB_management(out_folder_path=work_dir, out_name='rotated_rasters.gdb')

### CREATING AN EMPTY MOSAIC DATASET, INTO WHICH FINAL PRODUCT RASTERS WILL BE LATER ADDED
# arcpy.management.CreateMosaicDataset(in_workspace, in_mosaicdataset_name, coordinate_system, {num_bands},
# {pixel_type}, {product_definition}, {product_band_definitions})
spRef_1 = arcpy.SpatialReference(26919)  # UTM coordinate system (26919 == NAD 1983 Zone 19N)
mosaic_ds = arcpy.CreateMosaicDataset_management(in_workspace=fileGDB, in_mosaicdataset_name='mosaic_dataset',
                                                 coordinate_system=spRef_1, num_bands=3, pixel_type='8_BIT_UNSIGNED',
                                                 product_definition='NATURAL_COLOR_RGB')
### DEFINING DIRECTORY PATHS
images_dir = os.path.join(work_dir, r'input_data\test_images')
output_dir = os.path.join(work_dir, 'output_files')

### DEFINING VARIABLES FOR SEARCH CURSOR OPERATIONS
input_shp = os.path.join(output_dir, 'image_coords_xy.shp')
fields = ['FileName', 'GSD_m', 'ULX', 'ULY', 'GimbalYaw']

count = 0

### SEARCH CURSOR USED TO LOOP THROUGH LIST OF IMAGES IN SHAPEFILE ATTRIBUTE TABLE;
### WORLD FILE GENERATED FOR GEOREFERENCING; IMAGES ROTATED AND MERGED TO MOSAIC DATASET
with arcpy.da.SearchCursor(input_shp, fields) as cursor:
    for row in cursor:

        ### DEFINING FIELD VARIABLES BY ROW INPUT
        jpg_filename = row[0]
        GSD = row[1]
        worldFile_X = row[2]
        worldFile_Y = row[3]
        rotation = row[4]

        ### DEFINING THE NAMING PROPERTIES AND OUTPUT LOCATION OF TEXT FILES
        txt_file = os.path.join(images_dir, jpg_filename.replace('.JPG', '.txt'))

        ### CREATING TEXT FILES TO BE CONVERTED AND USED AS WORLD FILE GEOREFERENCING INSTRUCTIONS
        with open(txt_file, 'w') as new_txt_file:
            new_txt_file.write(str(GSD) + '\n0\n0\n' + '-' + str(GSD) + '\n' + str(worldFile_X) + '\n' + str(worldFile_Y))

        ### ALTERING TEXT FILE EXTENSION TO .JGW (THIS ALTERATION DEFINES IT AS A WORLD FILE, RECOGNIZED BY ARCGIS)
        filename_no_ext = os.path.join(images_dir, jpg_filename.replace('.JPG', ''))
        os.rename(txt_file, filename_no_ext + '.jgw')

        # ### MOVING IMAGES INTO A FILE GEODATABASE PRIOR TO ROTATION AND MERGING INTO MOSAIC DATASET
        # # arcpy.conversion.RasterToGeodatabase(Input_Rasters, Output_Geodatabase, {Configuration_Keyword})
        # image_in = os.path.join(images_dir, jpg_filename)
        # arcpy.RasterToGeodatabase_conversion(Input_Rasters=image_in, Output_Geodatabase=fileGDB)

        ### DEFINING NEW NAME FOR ROTATED RASTER AND RESOLVING ESRI GRID STACK FORMAT CHARACTER LIMIT
        pre_rotate_raster = os.path.join(images_dir, jpg_filename)
        count = count + 1
        image = "image_" + str(count)
        GDB_rotate_raster = os.path.join(fileGDB, image)

        ### ROTATING RASTERS
        # arcpy.management.Rotate(in_raster, out_raster, angle, {pivot_point}, {resampling_type}, {clipping_extent})
        arcpy.Rotate_management(in_raster=pre_rotate_raster, out_raster=GDB_rotate_raster, angle=rotation)

        ### ADDING RASTERS TO MOSAIC DATASET
        # arcpy.management.AddRastersToMosaicDataset(in_mosaic_dataset, raster_type, input_path, {update_cellsize_ranges},
        # {update_boundary}, {update_overviews}, {maximum_pyramid_levels}, {maximum_cell_size}, {minimum_dimension},
        # {spatial_reference}, {filter}, {sub_folder}, {duplicate_items_action}, {build_pyramids}, {calculate_statistics},
        # {build_thumbnails}, {operation_description}, {force_spatial_reference}, {estimate_statistics}, {aux_inputs},
        # {enable_pixel_cache}, {cache_location})
        spRef_2 = arcpy.SpatialReference(4326)  # (4326 == WGS 1984)
        arcpy.AddRastersToMosaicDataset_management(in_mosaic_dataset=mosaic_ds, raster_type="UAV/UAS",
                                                   input_path=GDB_rotate_raster, spatial_reference=spRef_2)

# arcpy.management.SetMosaicDatasetProperties(in_mosaic_dataset, {rows_maximum_imagesize}, {columns_maximum_imagesize},
# {allowed_compressions}, {default_compression_type}, {JPEG_quality}, {LERC_Tolerance}, {resampling_type},
# {clip_to_footprints}, {footprints_may_contain_nodata}, {clip_to_boundary}, {color_correction},
# {allowed_mensuration_capabilities}, {default_mensuration_capabilities}, {allowed_mosaic_methods},
# {default_mosaic_method}, {order_field}, {order_base}, {sorting_order}, {mosaic_operator}, {blend_width},
# {view_point_x}, {view_point_y}, {max_num_per_mosaic}, {cell_size_tolerance}, {cell_size}, {metadata_level},
# {transmission_fields}, {use_time}, {start_time_field}, {end_time_field}, {time_format}, {geographic_transform},
# {max_num_of_download_items}, {max_num_of_records_returned}, {data_source_type}, {minimum_pixel_contribution},
# {processing_templates}, {default_processing_template}, {time_interval}, {time_interval_units}, {product_definition},
# {product_band_definitions})
