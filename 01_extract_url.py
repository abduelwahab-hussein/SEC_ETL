# Script Description:
# This script extracts NPORT URLs from SEC filings and saves them into a structured text file for further processing.
# Each URL corresponds to an SEC form available on the SEC website. The forms are stored in year-specific folders.
# The script processes input files containing NPORT filings, searches for specific keywords related to the form type,
# and outputs the extracted URLs for each year into a corresponding text file.
#
# Usage:
# - Update the 'years' list with the desired years to process.
# - Ensure that the input files for each year are stored in the corresponding directory named after the year.
# - Keywords for NPORT forms are hardcoded in the script; adjust if needed to include additional form types.

import os

# Define the years to process
years = ['2019', '2020', '2021', '2022', '2023']

# Initialize a counter for breaks
breaks = 1

# Loop through each year to process its files
for year in years:
    dir_path = f"/working_directory/{year}"

    # List all files in the directory
    file_list = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    for file_name in file_list:
        file_path = os.path.join(dir_path, file_name)

        # Open and read the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        print(lines)

        # Create an output file for extracted URLs
        with open(f"output_{year}_no_nt.txt", "a") as txt_file:
            for line in lines:
                # Check if the line contains any of the target NPORT keywords
                if 'NPORT-P|' in line or 'NPORT-P/A|' in line or \
                   'NPORT-NP|' in line or 'NPORT-NP/A|' in line:

                    breaks += 1

                    # Stop processing after 10 matches (for debugging or limits)
                    if breaks == 10:
                        break

                    # Extract the portion of the line containing the SEC URL
                    index = line.index('edgar/data/')
                    print(line)
                    print(index)
                    print(line[index:])

                    edgar_url = line[index:].strip()
                    print(edgar_url)

                    # Write the extracted URL to the output file
                    txt_file.write(f"https://www.sec.gov/Archives/{edgar_url}\n")
