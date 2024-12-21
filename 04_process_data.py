# Script Description:
# This script processes XML data from NPORT filings by extracting relevant information for various sections,
# such as headers, general information, fund details, and securities data. It maps XML tags to a structured
# data format, handling optional fields and saving the processed data into CSV files.
# NPORT XML schema can be found here: https://www.sec.gov/info/edgar/specifications/form-n-port-xml-tech-specs.htm
# NPORT PDF Form can be found here:https://www.sec.gov/files/formn-port.pdf

from bs4 import BeautifulSoup
import pandas as pd
import os

# Initialize paths and data structures
dir_path = "/path/to/nport_data"
header_data, general_data, fund_data, securities_data = [], [], [], []

# Header mapping
header_mapping = {
    "form_type": "submissionType",
    "confidential": "isConfidential",
}

# General mapping
general_mapping = {
    "registrant_name": "regName",
    "registrant_file_number": "regFileNumber",
    "registrant_cik": "regCik",
    "registrant_street": "regStreet1",
    "registrant_city": "regCity",
    "registrant_code": "regZipOrPostalCode",
}

# Fund mapping
fund_mapping = {
    "assets": "totAssets",
    "liabilities": "totLiabs",
    "net_assets": "netAssets",
}

# Securities mapping
securities_mapping = {
    "name": "name",
    "cusip": "cusip",
    "balance": "balance",
    "units": "units",
}

# Deep securities mapping
deep_securities_mapping = {
    "debt_maturity_date": {"tag_name": "debtSec", "subtag_name": "maturityDt"},
    "debt_coupon_type": {"tag_name": "debtSec", "subtag_name": "couponKind"},
    "debt_annualized_rate": {"tag_name": "debtSec", "subtag_name": "annualizedRt"},
    "default": {"tag_name": "debtSec", "subtag_name": "isDefault"},
    "arrears": {"tag_name": "debtSec", "subtag_name": "areIntrstPmtsInArrs"},
}

# Securities attribute mapping
securities_attribute_mapping = {
    "currency_other": {"tag_name": "currencyConditional", "attribute_name": "curCd"},
    "exchange_rate": {"tag_name": "currencyConditional", "attribute_name": "exchangeRt"},
    "asset_category_alt": {"tag_name": "assetConditional", "attribute_name": "assetCat"},
    "asset_description": {"tag_name": "assetConditional", "attribute_name": "desc"},
    "issuer_category_alt": {"tag_name": "issuerConditional", "attribute_name": "issuerCat"},
    "issuer_description": {"tag_name": "issuerConditional", "attribute_name": "desc"},
}

# Deep securities attribute mapping
deep_securities_attribute_mapping = {
    "isin": {"tag_name": "identifiers", "subtag_name": "isin", "attribute_name": "value"},
    "ticker": {"tag_name": "identifiers", "subtag_name": "ticker", "attribute_name": "value"},
    "other_id": {"tag_name": "identifiers", "subtag_name": "other", "attribute_name": "value"},
    "other_id_details": {"tag_name": "identifiers", "subtag_name": "other", "attribute_name": "desc"},
}

# File processing
for filename in os.listdir(dir_path):
    file_path = os.path.join(dir_path, filename)

    # Extract accession number
    accession_number = filename[:-4]
    print(filename)

    with open(file_path, "r") as file:
        contents = file.read()

        # Find date filed
        index_file_date = contents.find("FILED AS OF DATE:")
        date_filed = contents[index_file_date + len("FILED AS OF DATE:") :].strip()

        soup = BeautifulSoup(contents, "xml")

        header = soup.find("headerData")
        general = soup.find("genInfo")
        fund = soup.find("fundInfo")
        securities = soup.find_all("invstOrSec")

        # Header mapping
        header_row = {"accession_number": accession_number}
        for variable, tag in header_mapping.items():
            try:
                header_row[variable] = header.find(tag).text
            except AttributeError:
                header_row[variable] = "n/a"

        header_data.append(header_row)

        # General mapping
        general_row = {"accession_number": accession_number}
        for variable, tag in general_mapping.items():
            try:
                general_row[variable] = general.find(tag).text
            except AttributeError:
                general_row[variable] = "n/a"

        general_data.append(general_row)

        # Fund mapping
        fund_row = {"accession_number": accession_number}
        for variable, tag in fund_mapping.items():
            try:
                fund_row[variable] = fund.find(tag).text
            except AttributeError:
                fund_row[variable] = "n/a"

        fund_data.append(fund_row)

        # Securities mapping
        for security in securities:
            row = {"accession_number": accession_number}

            # Basic securities mapping
            for variable, tag in securities_mapping.items():
                try:
                    row[variable] = security.find(tag).text
                except AttributeError:
                    row[variable] = "n/a"

            # Deep securities mapping
            for variable, mapping_info in deep_securities_mapping.items():
                try:
                    tag = security.find(mapping_info["tag_name"])
                    subtag = tag.find(mapping_info["subtag_name"]).text
                    row[variable] = subtag
                except (AttributeError, TypeError):
                    row[variable] = "n/a"

            # Attribute mapping
            for variable, mapping_info in securities_attribute_mapping.items():
                try:
                    row[variable] = security.find(mapping_info["tag_name"])[
                        mapping_info["attribute_name"]
                    ]
                except (AttributeError, TypeError):
                    row[variable] = "n/a"

            # Deep attribute mapping
            for variable, mapping_info in deep_securities_attribute_mapping.items():
                try:
                    tag = security.find(mapping_info["tag_name"])
                    subtag = tag.find(mapping_info["subtag_name"]).text
                    attribute = subtag[mapping_info["attribute_name"]]
                    row[variable] = attribute
                except (AttributeError, TypeError):
                    row[variable] = "n/a"

            securities_data.append(row)

# Save extracted data to CSV files
df0 = pd.DataFrame(header_data)
df0.to_csv("header_data.csv", index=False)

df1 = pd.DataFrame(general_data)
df1.to_csv("general_data.csv", index=False)

df2 = pd.DataFrame(fund_data)
df2.to_csv("fund_data.csv", index=False)

df3 = pd.DataFrame(securities_data)
df3.to_csv("securities_data.csv", index=False)
