#### NRS-528 #######################
#### Semester Final Coding Challenge
############################ Tool #3

import os
import sys
import arcpy
from colorama import Fore

### DEFINE GEODATABASE WORKSPACE CONTAINING RASTERS
arcpy.env.workspace = work_dir = sys.argv[1]

fileGDB = os.path.join(work_dir, 'DGtool_Outputs.gdb')

### ALLOW OVERWRITING OF ARCGIS PRO OUTPUTS
arcpy.env.overwriteOutput = False

### DEFINE SPATIAL REFERENCE FOR GEOPROCESSING TASKS
spRef = arcpy.SpatialReference(26919)  # 26919 = NAD 1983 Zone 19N; UTMs needed for world file format correspondence

### CREATE MOSAIC DATASET
mosaic_ds = arcpy.CreateMosaicDataset_management(in_workspace=fileGDB,
                                                 in_mosaicdataset_name='mosaic_dataset',
                                                 coordinate_system=spRef,
                                                 num_bands=3, pixel_type='8_BIT_UNSIGNED',
                                                 product_definition='NATURAL_COLOR_RGB')
# arcpy.management.CreateMosaicDataset(in_workspace, in_mosaicdataset_name, coordinate_system, {num_bands},
#                                      {pixel_type}, {product_definition}, {product_band_definitions})
if arcpy.Exists(mosaic_ds):
    print(Fore.GREEN + "\nEmpty mosaic dataset generated ..." + Fore.RESET)

### SET MOSAIC DATASET PROPERTIES
mds_prop = arcpy.SetMosaicDatasetProperties_management(in_mosaic_dataset=mosaic_ds,
                                                       footprints_may_contain_nodata='FOOTPRINTS_DO_NOT_CONTAIN_NODATA',
                                                       default_mosaic_method='Center',
                                                       mosaic_operator='FIRST')
# arcpy.management.SetMosaicDatasetProperties(in_mosaic_dataset, {rows_maximum_imagesize}, {columns_maximum_imagesize},
#       {allowed_compressions}, {default_compression_type}, {JPEG_quality}, {LERC_Tolerance}, {resampling_type},
#       {clip_to_footprints}, {footprints_may_contain_nodata}, {clip_to_boundary}, {color_correction},
#       {allowed_mensuration_capabilities}, {default_mensuration_capabilities}, {allowed_mosaic_methods},
#       {default_mosaic_method}, {order_field}, {order_base}, {sorting_order}, {mosaic_operator}, {blend_width},
#       {view_point_x}, {view_point_y}, {max_num_per_mosaic}, {cell_size_tolerance}, {cell_size}, {metadata_level},
#       {transmission_fields}, {use_time}, {start_time_field}, {end_time_field}, {time_format}, {geographic_transform},
#       {max_num_of_download_items}, {max_num_of_records_returned}, {data_source_type}, {minimum_pixel_contribution},
#       {processing_templates}, {default_processing_template}, {time_interval}, {time_interval_units},
#       {product_definition}, {product_band_definitions})

if arcpy.Exists(mds_prop):
    print(Fore.GREEN + "\nMosaic dataset properties defined ..." + Fore.RESET)

### ADD RASTERS TO MOSAIC DATASET
add_to_mds = arcpy.AddRastersToMosaicDataset_management(in_mosaic_dataset=mosaic_ds,
                                                        raster_type='Raster Dataset',
                                                        input_path=fileGDB,
                                                        update_overviews='UPDATE_OVERVIEWS',
                                                        enable_pixel_cache='USE_PIXEL_CACHE')
# arcpy.management.AddRastersToMosaicDataset(in_mosaic_dataset, raster_type, input_path, {update_cellsize_ranges},
#       {update_boundary}, {update_overviews}, {maximum_pyramid_levels}, {maximum_cell_size}, {minimum_dimension},
#       {spatial_reference}, {filter}, {sub_folder}, {duplicate_items_action}, {build_pyramids}, {calculate_statistics},
#       {build_thumbnails}, {operation_description}, {force_spatial_reference}, {estimate_statistics}, {aux_inputs},
#       {enable_pixel_cache}, {cache_location})

if arcpy.Exists(add_to_mds):
    print(Fore.GREEN + "\nRasters added to mosaic dataset ..." + Fore.RESET)

### UPDATE MOSAIC DATASET FOOTPRINTS AND BOUNDARY
mds_foot = arcpy.BuildFootprints_management(in_mosaic_dataset=mosaic_ds)
# arcpy.management.BuildFootprints(in_mosaic_dataset, {where_clause}, {reset_footprint}, {min_data_value},
#       {max_data_value}, {approx_num_vertices}, {shrink_distance}, {maintain_edges}, {skip_derived_images},
#       {update_boundary}, {request_size}, {min_region_size}, {simplification_method}, {edge_tolerance},
#       {max_sliver_size}, {min_thinness_ratio})

if arcpy.Exists(mds_foot):
    print(Fore.GREEN + "\nNew raster footprints and dataset boundary generated ..." + Fore.RESET)

if arcpy.Exists(mosaic_ds and mds_prop and add_to_mds and mds_foot):
    print(Fore.CYAN + "\nMosaic dataset complete, output to file geodatabase:\n" + Fore.RESET + fileGDB)
