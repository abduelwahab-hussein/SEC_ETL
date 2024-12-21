# SEC_ETL

## Functionality:
Python code that provides a comprehensive and efficient way o extract, process, and organize data from publicly available SEC filings into clean datasets. We use SEC N-PORT filings as an example.

## Use Cases:
Geared towards finance professionals, researchers, academics, or anyone looking to analyze aggregate or specific SEC data on financial institutions.


## Code Walk-through:
### 01_extract_URL.py: 
This code block identifies and extracts URLs from SEC filings and saves them into year-specific output files.

### 02_download_forms.py: 
Automates downloading forms from extracted URLs and organizes them into year-specific folders.

### 03_process_funds.py (optional): 
Filters downloaded files based on specific SEC Series IDs, copying relevant files into a dedicated folder.

### 04_process_data.py: 
Extracts data from SEC filings, such as general data, fund details, and securities attributes, and organizes it into clean dataset for further analysis


