# Script Description:
# This script processes SEC filing directories organized by year to identify and copy specific fund-related files.
# It scans through files in year-specific folders, searches for a specific SEC series ID,
# and copies any matching files to a designated directory for further analysis.
#
# Usage:
# - Update the 'years' list with the years corresponding to the folders to process.
# - Set the 'specific_funds_path' variable to the desired output directory where matched files will be copied.
# - Replace `{target_sec_id}` in 'sec_series_id' with the SEC series ID(s) you are searching for.
# - Ensure that the input directories are structured as `/year/filename.txt`.
# - The script will create a copy of matching files in 'specific_funds_path'.

import os
import shutil

# List of years for which to process files
years = ['2019', '2020', '2021', '2022', '2023', '2024']

# Define the directory where matched files will be copied
specific_funds_path = '/path/to/your/output/directory'

# Define the SEC series IDs to search for
sec_series_id = ["<seriesId>S000062359</seriesId>", "<seriesId>S000031341</seriesId>", "<seriesId>S000019373</seriesId>"]

# Iterate over each year folder
for year in years:
    dir_path = f"/path/to/working_directory/{year}"

    # List all files in the year-specific directory
    file_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    # Process each file in the directory
    for filename in file_list:
        file_path = os.path.join(dir_path, filename)

        # Open and read the file content
        with open(file_path, 'r') as file:
            lines = file.read()

        # Check for specific SEC series IDs in the file
        specific_funds_found = False
        for series_id in sec_series_id:
            if series_id in lines:
                specific_funds_found = True
                break

        # If a specific fund is found, copy the file to the output directory
        if specific_funds_found:
            shutil.copy(file_path, specific_funds_path)
