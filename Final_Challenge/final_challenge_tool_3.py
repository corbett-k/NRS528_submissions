#### NRS-528 #######################
#### Semester Final Coding Challenge
############################ Tool #3

import arcpy
from colorama import Fore

### DEFINE GEODATABASE WORKSPACE CONTAINING RASTERS
fileGDB = r'C:\Users\krist\Documents\GitHub\NRS528_submissions\Final_Challenge\DGtool_Outputs.gdb'
arcpy.env.workspace = fileGDB

### ALLOW OVERWRITING OF ARCGIS PRO OUTPUTS
arcpy.env.overwriteOutput = True

### DEFINE SPATIAL REFERENCE FOR GEOPROCESSING TASKS
spRef = arcpy.SpatialReference(26919)  # 26919 = NAD 1983 Zone 19N; UTMs required for WF format correspondence

### CREATE MOSAIC DATASET
mosaic_ds = arcpy.CreateMosaicDataset_management(in_workspace=fileGDB, in_mosaicdataset_name='mosaic_dataset',
                                                 coordinate_system=spRef, num_bands=3, pixel_type='8_BIT_UNSIGNED',
                                                 product_definition='NATURAL_COLOR_RGB')
# arcpy.management.CreateMosaicDataset(in_workspace, in_mosaicdataset_name, coordinate_system, {num_bands},
#                                      {pixel_type}, {product_definition}, {product_band_definitions})
if arcpy.Exists(mosaic_ds):
    print(Fore.GREEN + "\nEmpty mosaic dataset generated ..." + Fore.RESET)

# ## ADDING RASTERS TO MOSAIC DATASET
arcpy.AddRastersToMosaicDataset_management(in_mosaic_dataset=mosaic_ds, raster_type='Raster Dataset', input_path=fileGDB,
                                           update_overviews='UPDATE_OVERVIEWS', enable_pixel_cache='USE_PIXEL_CACHE')
# arcpy.management.AddRastersToMosaicDataset(in_mosaic_dataset, raster_type, input_path, {update_cellsize_ranges},
#                                            {update_boundary}, {update_overviews}, {maximum_pyramid_levels},
#                                            {maximum_cell_size}, {minimum_dimension}, {spatial_reference}, {filter},
#                                            {sub_folder}, {duplicate_items_action}, {build_pyramids}, {calculate_statistics},
#                                            {build_thumbnails}, {operation_description}, {force_spatial_reference},
#                                            {estimate_statistics}, {aux_inputs}, {enable_pixel_cache}, {cache_location})

print(Fore.GREEN + "\nRasters added to mosaic dataset ...\nSetting mosaic dataset properties ..." + Fore.RESET)

arcpy.SetMosaicDatasetProperties_management(in_mosaic_dataset=mosaic_ds, default_mosaic_method='Center', mosaic_operator='FIRST')
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

print(Fore.GREEN + "\nMosaic dataset properties defined ...\nReady for display and interpretation..." +
      Fore.CYAN + "\n\nMosaic dataset complete, located in following file geodatabase:\n" + Fore.RESET + fileGDB)
