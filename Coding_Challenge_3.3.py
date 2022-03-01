# Coding Challenge 3.3: Working with CSV

# Using the Atmospheric Carbon Dioxide Dry Air Mole Fractions from quasi-continuous daily measurements at Mauna Loa,
# Hawaii dataset, obtained from here (https://github.com/datasets/co2-ppm-daily/tree/master/data).
# Using Python (csv) calculate the following:
# 1. Annual average for each year in the dataset.
# 2. Minimum, maximum and average for the entire dataset.
# 3. Seasonal average if Spring (March, April, May), Summer (June, July, August), Autumn (September, October, November)
#    and Winter (December, January, February).
# 4. Calculate the anomaly for each value in the dataset relative to the mean for the entire time series.

import csv

years = []
months = []
CO2_values = []

# Calculating Minimum / Maximum / Mean Values:

with open("co2-ppm-daily.csv") as CO2:
    csv_reader = csv.reader(CO2, delimiter=',')
    line_counter = 0
    header_skip = next(CO2)
    print(header_skip)

    for row in csv_reader:
        year, month, day = row[0].split("-")
        if year not in years:
            years.append(year)
        if month not in months:
            months.append(month)

        CO2_values.append(float(row[1]))
        line_counter = line_counter + 1

print("The maximum CO2 value from the list is " + str(max(CO2_values)))
print("\nThe minimum CO2 value from the list is " + str(min(CO2_values)))
print("\nThe average of all CO2 values from the list is " + str(float(sum(CO2_values) / int(line_counter))))

# Calculating Annual Averages:

years_dict = {}

for year in years:
    years_list = []
    with open("co2-ppm-daily.csv") as CO2:
        csv_reader = csv.reader(CO2, delimiter=',')
        header_skip = next(CO2)

        for row in csv_reader:
            CO2_year, CO2_month, CO2_day = row[0].split("-")
            if CO2_year == year:
                years_list.append(float(row[1]))

    years_dict[year] = str(str(sum(years_list) / len(years_list)))

print("\nThe following are average annual CO2 values from 1958-2019:\n" + str(years_dict))

# Calculating Seasonal Averages:

spring_list = []
summer_list = []
autumn_list = []
winter_list = []

with open("co2-ppm-daily.csv") as CO2:
    csv_reader = csv.reader(CO2, delimiter=',')
    header_skip = next(CO2)

    for row in csv_reader:
        CO2_year, CO2_month, CO2_day = row[0].split("-")
        if CO2_month == '03' or CO2_month == '04' or CO2_month == '05':
            spring_list.append(float(row[1]))
        if CO2_month == '06' or CO2_month == '07' or CO2_month == '08':
            summer_list.append(float(row[1]))
        if CO2_month == '09' or CO2_month == '10' or CO2_month == '11':
            autumn_list.append(float(row[1]))
        if CO2_month == '12' or CO2_month == '01' or CO2_month == '02':
            winter_list.append(float(row[1]))

print("\nThe average CO2 value throughout Spring months in this dataset = " + str(sum(spring_list) / len(spring_list)))
print("\nThe average CO2 value throughout Summer months in this dataset = " + str(sum(summer_list) / len(summer_list)))
print("\nThe average CO2 value throughout Autumn months in this dataset = " + str(sum(autumn_list) / len(autumn_list)))
print("\nThe average CO2 value throughout Winter months in this dataset = " + str(sum(winter_list) / len(winter_list)))

# Calculating Anomalies:

overall_avg = sum(CO2_values) / len(CO2_values)
anomaly_dict = {}

with open("co2-ppm-daily.csv") as CO2:
    csv_reader = csv.reader(CO2, delimiter=',')
    header_skip = next(CO2)

    for row in csv_reader:
        CO2_year, CO2_month, CO2_day = row[0].split("-")
        anomaly_dict[CO2_year, CO2_month, CO2_day] = float(row[1]) - overall_avg

print(anomaly_dict)

## Also worked on outputting to a new csv, but I'd like to learn how to recombine the dates to original format; for some
## the output .csv skips every other row; otherwise it more or less worked
#
# with open("Coding_Challenge_3.3_anomaly_values.csv", "w") as csvfile:
#     writer = csv.writer(csvfile)
#     for date, value in anomaly_dict.items():
#         writer.writerow([date, value])
#     csvfile.close()
