## Coding
#### Challenge
###### 9

import arcpy
from colorama import Fore, Back, Style

arcpy.env.workspace = r'C:\Users\Kristopher\Documents\Repos\528submissionsRepo\Coding_Challenge_9\RI_FHWP_all_pts_invasives'

input_shp = r'C:\Users\Kristopher\Documents\Repos\528submissionsRepo\Coding_Challenge_9\RI_FHWP_all_pts_invasives\RI_FHWP_all_pts_invasives.shp'

# Task 1. (a) count how many individual records have photos, and (b) how many do not.

# (a)
fields = ['Site', 'Other']
expression = arcpy.AddFieldDelimiters(input_shp, "Other") + " = 'Photo' Or Other = 'Photos' Or Other = 'PHOTO'"

yes_photo = []
no_photo = []
count = 1

with arcpy.da.SearchCursor(input_shp, fields, expression) as cursor:
    for row in cursor:
        if row[0] not in yes_photo:
            yes_photo.append(row[0])
        # print(str(count) + u'. {0}: {1}'.format(row[0], row[1]))
        count += 1

print(Fore.BLUE + "\nThere are " + Fore.RESET + str(count - 1) + Fore.BLUE + " individual records with photos, for the"
                  " following " + Fore.RESET + str(len(yes_photo)) + Fore.BLUE + " sites:\n" + Fore.RESET + str(yes_photo))

in_layer_or_view = input_shp
selection_type = "NEW SELECTION"
where_clause = "Other = 'Photo' Or Other = 'Photos' Or Other = 'PHOTO'"
lyr = arcpy.management.SelectLayerByAttribute(in_layer_or_view, selection_type, where_clause)
cpy_lyr = 'RI_FHWP_invasives_pts_yesPhotos.shp'
arcpy.CopyFeatures_management(lyr, cpy_lyr)

if arcpy.Exists(cpy_lyr):
    print("\n" + Fore.BLACK + Back.CYAN + "point shapefile successfully generated for records with photos..." + Style.RESET_ALL + "\n")

# (b)
expression = arcpy.AddFieldDelimiters(input_shp, "Other") + " <> 'Photo' And Other <> 'Photos' And Other <> 'PHOTO'"
no_photo = []
count = 1

with arcpy.da.SearchCursor(input_shp, fields, expression) as cursor:
    for row in cursor:
        if row[0] not in no_photo:
            no_photo.append(row[0])
        # print(str(count) + u'. {0}: {1}'.format(row[0], row[1]))
        count += 1

print(Fore.RED + "There are " + Fore.RESET + str(count - 1) + Fore.RED + " individual records without photos, for the"
                  " following " + Fore.RESET + str(len(no_photo)) + Fore.RED + " sites:\n" + Fore.RESET + str(no_photo))

in_layer_or_view = input_shp
selection_type = "NEW SELECTION"
where_clause = "Other <> 'Photo' And Other <> 'Photos' And Other <> 'PHOTO'"
lyr = arcpy.management.SelectLayerByAttribute(in_layer_or_view, selection_type, where_clause)
cpy_lyr = 'RI_FHWP_invasives_pts_noPhotos.shp'
arcpy.CopyFeatures_management(lyr, cpy_lyr)

if arcpy.Exists(cpy_lyr):
    print("\n" + Fore.BLACK + Back.CYAN + "point shapefile successfully generated for records without photos..." + Style.RESET_ALL + "\n")


# # 2.	Count how many unique species there are in the dataset, print the result.

fields = ['Species']
expression = arcpy.AddFieldDelimiters(input_shp, "Species") + " NOT LIKE ' %'"
sp_list = []

with arcpy.da.SearchCursor(input_shp, fields, expression) as cursor:
    for row in cursor:
        if row[0] not in sp_list:
            sp_list.append(row[0])
        # print(u'{0}'.format(row[0]))

print(Fore.GREEN + "There are " + Fore.RESET + str(len(sp_list)) + Fore.GREEN +
      " unique species in the dataset:\n" + Fore.RESET + str(sp_list))

