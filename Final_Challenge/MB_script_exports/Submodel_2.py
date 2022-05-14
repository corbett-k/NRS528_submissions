# -*- coding: utf-8 -*-
"""
Generated by ArcGIS ModelBuilder on : 2022-05-14 12:57:51
"""
import arcpy
from sys import argv
def #  NOT  IMPLEMENTED# Function Body not implemented
def parseName (name):
	return str(name).rstrip(".JPG")
def Rotate(inRaster, outRaster, angle, X, Y):
	arcpy.Rotate_management(inRaster, outRaster, angle, "%s %s" % (X, Y))
	return outRaster

def Submodel():  # Submodel

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"C:\Users\krist\Documents\ArcGIS\Projects\toolboxes\modified\Ashley_CFproject.tbx")
    # Model Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"C:\Users\krist\Documents\ArcGIS\Projects\toolboxes\Woodcock\Woodcock.gdb", workspace=r"C:\Users\krist\Documents\ArcGIS\Projects\toolboxes\Woodcock\Woodcock.gdb"):
        _Value_ = arcpy.Raster("")
        Point_Feature_Class_center_pixel_ = ""
        txt_files_out = ""

        for Point_Feature_Class_Iteration, Value in #  NOT  IMPLEMENTED(Point_Feature_Class_center_pixel_, [["FileName", ""]], False):

            # Process: Remove Filename Extension (Calculate Value) ()
            if Value:
                with arcpy.EnvManager(scratchWorkspace=r"C:\Users\krist\OneDrive\Desktop\georef_tool\georef_tool.gdb", workspace=r"C:\Users\krist\OneDrive\Desktop\georef_tool\georef_tool.gdb"):
                    Name = parseName("Value")

            # Process: Table To Table (Table To Table) (conversion)
            if Name and Value:
                with arcpy.EnvManager(scratchWorkspace=r"C:\Users\krist\Documents\ArcGIS\Projects\Woodcock\Woodcock.gdb", workspace=r"C:\Users\krist\Documents\ArcGIS\Projects\Woodcock\Woodcock.gdb"):
                    _Name_txt = arcpy.conversion.TableToTable(in_rows=Point_Feature_Class_Iteration, out_path=txt_files_out, out_name=f"{Name}.txt", where_clause="", field_mapping="GSD_m \"GSD_m\" true true false 8 Double 0 0,First,#,I_image_metadata_XYTableToPoint_FileName,GSD_m,-1,-1;ULX \"ULX\" true true false 8 Double 0 0,First,#,I_image_metadata_XYTableToPoint_FileName,ULX,-1,-1;ULY \"ULY\" true true false 8 Double 0 0,First,#,I_image_metadata_XYTableToPoint_FileName,ULY,-1,-1", config_keyword="")[0]

            # Process: Format World File (Format World File) (GeorefToolDroneDeploy)
            Name = "1"
            _Name_jgw = fr"C:\Users\krist\Documents\ArcGIS\Projects\custom_georef_tool\input_data\wide\{Name}.jgw"
            if Name and Value:
                with arcpy.EnvManager(scratchWorkspace=r"C:\Users\krist\Documents\ArcGIS\Projects\Ashley_CFproject\Ashley_CFproject.gdb", workspace=r"C:\Users\krist\Documents\ArcGIS\Projects\Ashley_CFproject\Ashley_CFproject.gdb"):
                    arcpy.GeorefToolDroneDeploy.FormatWF(Input=_Name_txt, Output=_Name_jgw)

            # Process: Copy Raster (Copy Raster) (management)
            _Name_ = fr"C:\Users\krist\Documents\ArcGIS\Projects\custom_georef_tool\beavertail_wide_rotated_rasters.gdb\{Name}"
            if Name and Value and _Name_jgw:
                with arcpy.EnvManager(compression="LZ77", outputCoordinateSystem="PROJCS["NAD_1983_UTM_Zone_19N",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-69.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]", pyramid="NONE", 
                                      rasterStatistics="NONE", scratchWorkspace=r"C:\Users\krist\Documents\ArcGIS\Projects\Woodcock\Woodcock.gdb", workspace=r"C:\Users\krist\Documents\ArcGIS\Projects\Woodcock\Woodcock.gdb"):
                    arcpy.management.CopyRaster(in_raster=_Value_, out_rasterdataset=_Name_, config_keyword="", background_value=None, nodata_value="256", onebit_to_eightbit="NONE", colormap_to_RGB="NONE", pixel_type="", scale_pixel_value="NONE", RGB_to_Colormap="NONE", format="JPEG", transform="Transform", process_as_multidimensional="CURRENT_SLICE", build_multidimensional_transpose="NO_TRANSPOSE")

            # Process: Get_Field_Value (Get Field Value) 
            # Get Field Value Utility is not implemented 

            # Process: Get_Field_Value_2_ (Get Field Value) 
            # Get Field Value Utility is not implemented 

            # Process: Get_Field_Value_3_ (Get Field Value) 
            # Get Field Value Utility is not implemented 

            # Process: Rotate Raster (Calculate Value) ()
            if Angle_of_Rotation and Name and Pivot_Point_X_Coordinate and Pivot_Point_Y_Coordinate and Value and _Name_ and _Name_jgw:
                with arcpy.EnvManager(scratchWorkspace=r"F:\Classes\NRS_522_2021\Modules\Lidar_Applications\Lidar_Applications.gdb", workspace=r"F:\Classes\NRS_522_2021\Modules\Lidar_Applications\Lidar_Applications.gdb"):
                    Rotated_Raster = Rotate(r'C:\Users\krist\Documents\ArcGIS\Projects\custom_georef_tool\beavertail_wide_rotated_rasters.gdb\Name', r'C:\Users\krist\Documents\ArcGIS\Projects\custom_georef_tool\beavertail_wide_rotated_rasters.gdb\Name_rotated', Angle_of_Rotation, Pivot_Point_X_Coordinate, Pivot_Point_Y_Coordinate)

            # Process: Delete (Delete) (management)
            if Angle_of_Rotation and Name and Pivot_Point_X_Coordinate and Pivot_Point_Y_Coordinate and Rotated_Raster and Value and _Name_ and _Name_jgw:
                with arcpy.EnvManager(scratchWorkspace=r"C:\Users\krist\Documents\ArcGIS\Projects\Woodcock\Woodcock.gdb", workspace=r"C:\Users\krist\Documents\ArcGIS\Projects\Woodcock\Woodcock.gdb"):
                    Delete_Succeeded = arcpy.management.Delete(in_data=[_Name_], data_type="")[0]

            return Delete_Succeeded

if __name__ == '__main__':
    Submodel(*argv[1:])