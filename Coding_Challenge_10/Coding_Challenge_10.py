## Coding
#### Challenge
###### 10


import os, arcpy

arcpy.env.workspace = r'C:\Users\krist\Documents\GitHub\NRS528_submissions\Coding_Challenge_10\Landsat_data_lfs'

rasterList = arcpy.ListRasters("LC*", "TIF")
# print(rasterList)

band_4_list = [raster for raster in rasterList if "_B5.tif" not in raster]
print(band_4_list)

band_5_list = [raster for raster in rasterList if "_B4.tif" not in raster]
print(band_5_list)

Feb_B4 = band_4_list[0]
print("\nFebruary Band 4 (Vis-Red) Raster: " + Feb_B4)
Feb_B5 = band_5_list[0]
print("    February Band 5 (NIR) Raster: " + Feb_B5)

Apr_B4 = band_4_list[1]
print("\n   April Band 4 (Vis-Red) Raster: " + Apr_B4)
Apr_B5 = band_5_list[1]
print("       April Band 5 (NIR) Raster: " + Apr_B5)

May_B4 = band_4_list[2]
print("\n     May Band 4 (Vis-Red) Raster: " + May_B4)
May_B5 = band_5_list[2]
print("         May Band 5 (NIR) Raster: " + May_B5)

July_B4 = band_4_list[3]
print("\n    July Band 4 (Vis-Red) Raster: " + July_B4)
July_B5 = band_5_list[3]
print("        July Band 5 (NIR) Raster: " + July_B5)

Oct_B4 = band_4_list[4]
print("\n October Band 4 (Vis-Red) Raster: " + Oct_B4)
Oct_B5 = band_5_list[4]
print("     October Band 5 (NIR) Raster: " + Oct_B5)

Nov_B4 = band_4_list[5]
print("\nNovember Band 4 (Vis-Red) Raster: " + Nov_B4)
Nov_B5 = band_5_list[5]
print("    November Band 5 (NIR) Raster: " + Nov_B5)

output_dir = r'C:\Users\krist\Documents\GitHub\NRS528_submissions\Coding_Challenge_10\output_files'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)
os.chdir(output_dir)

Feb_NDVI = arcpy.ia.RasterCalculator([Feb_B5, Feb_B4], ['x', 'y'], '(x-y)/(x+y)')
Feb_NDVI.save(os.path.join(output_dir, "Feb_NDVI.tif"))
if arcpy.Exists(Feb_NDVI):
    print("\nNDVI raster generated from February 2015 Landsat bands 4 & 5 ...")

Apr_NDVI = arcpy.ia.RasterCalculator([Apr_B5, Apr_B4], ['x', 'y'], '(x-y)/(x+y)')
Apr_NDVI.save(os.path.join(output_dir, "Apr_NDVI.tif"))
if arcpy.Exists(Apr_NDVI):
    print("NDVI raster generated from April 2015 Landsat bands 4 & 5 ...")

May_NDVI = arcpy.ia.RasterCalculator([May_B4,May_B5], ['x', 'y'], '(x-y)/(x+y)')
May_NDVI.save(os.path.join(output_dir, "May_NDVI.tif"))
if arcpy.Exists(May_NDVI):
    print("NDVI raster generated from May 2015 Landsat bands 4 & 5 ...")

July_NDVI = arcpy.ia.RasterCalculator([July_B5, July_B4], ['x', 'y'], '(x-y)/(x+y)')
July_NDVI.save(os.path.join(output_dir, "July_NDVI.tif"))
if arcpy.Exists(July_NDVI):
    print("NDVI raster generated from July 2015 Landsat bands 4 & 5 ...")

Oct_NDVI = arcpy.ia.RasterCalculator([Oct_B5, Oct_B4], ['x', 'y'], '(x-y)/(x+y)')
Oct_NDVI.save(os.path.join(output_dir, "Oct_NDVI.tif"))
if arcpy.Exists(Oct_NDVI):
    print("NDVI raster generated from October 2015 Landsat bands 4 & 5 ...")

Nov_NDVI = arcpy.ia.RasterCalculator([Nov_B5, Nov_B4], ['x', 'y'], '(x-y)/(x+y)')
Nov_NDVI.save(os.path.join(output_dir, "Nov_NDVI.tif"))
if arcpy.Exists(Nov_NDVI):
    print("NDVI raster generated from November 2015 Landsat bands 4 & 5 ...")
