# Script Description:
# This script downloads SEC NPORT forms for specified years from a list of URLs provided in year-specific files.
# Each URL corresponds to an SEC form stored on the SEC website. The forms are truncated to include only the
# content up to the first occurrence of '</DOCUMENT>', and they are saved in year-specific folders.
# Additionally, the script filters the forms based on a list of SEC series IDs to ensure relevant content is downloaded.
#
# Usage:
# - Update the 'years' list with the desired years.
# - Ensure that files named 'output_<year>_new_nt.txt' exist, containing the list of URLs for each year.
# - Replace 'your_email@example.com' with a valid email address for the User-Agent header.

import os
import time
import requests

# Download NPORT forms into their respective folders
years = ['2022', '2023', '2024']

breaks = 0  # Initialize breaks counter

def download_nport_forms(years):
    for year in years:
        # Define the download folder for the year
        download_folder = f"{year}_downloads"
        os.makedirs(download_folder, exist_ok=True)  # Create folder if it doesn't exist

        # Open the file containing URLs for the year
        with open(f"output_{year}_new_nt.txt", 'r') as output_file:
            urls = output_file.readlines()

        # List of SEC series IDs to match
        sec_series_ids = [
            '<seriesId>S000062359</seriesId>',
            '<seriesId>S000031341</seriesId>',
            '<seriesId>S000019373</seriesId>'
        ]

        # Set a delay between downloads to comply with SEC rate limits
        delay = 0.2  # seconds

        for url in urls:
            url = url.strip()  # Remove whitespace

            if url.startswith('http'):
                # Download content from the URL
                data = requests.get(url, headers={'User-Agent': 'your_email@example.com'})
                time.sleep(delay)

                text = data.text  # Get the response content as text
                print(text)  # Debug print to inspect content

                # Find the first instance of '</DOCUMENT>'
                index = text.find('</DOCUMENT>')

                # Check if the series ID matches
                for series_id in sec_series_ids:
                    if series_id in text:
                        # If the series ID is found and '</DOCUMENT>' exists, truncate the text
                        if index != -1:
                            truncated_text = text[:index]

                            # Extract filename from the URL
                            filename = os.path.join(download_folder, os.path.basename(url))

                            # Save the truncated content to a text file
                            with open(filename, 'w') as downloaded_file:
                                downloaded_file.write(truncated_text)

if __name__ == "__main__":
    download_nport_forms(years)
