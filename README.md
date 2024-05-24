---

# Bitcoin Address Checker

## Overview

Bitcoin Address Checker is a Python-based graphical user interface (GUI) application that allows users to validate and query Bitcoin addresses. The application reads a list of Bitcoin addresses from a file, validates them, and then fetches their transaction details from Blockchain.info. The results are displayed in a table and can be exported to a CSV file.

## Features

- **Load Bitcoin Addresses**: Load a list of Bitcoin addresses from a text file.
- **Validate Addresses**: Validate the format of the Bitcoin addresses.
- **Query Blockchain Data**: Query transaction details for the addresses from Blockchain.info.
- **Display Results**: Display the results in a sortable table within the GUI.
- **Export Results**: Export the results to a CSV file.

## Prerequisites

- Python 3.x
- PyQt5
- Requests

## Installation

1. Download the script.

2. Install the required Python packages:

   ```bash
   pip install PyQt5 requests
   ```

## Usage

1. Run the application:

   ```bash
   python BULK-BITCOIN-TXS.py
   ```

2. Use the GUI to:
   - **Select a file** containing Bitcoin addresses.
   - **Submit addresses** to validate and fetch data.
   - **Export results** to a CSV file.

## File Format

The input file should be a text file (.txt) with one Bitcoin address per line.
The script will perform a check to make sure each line is a valid Bitcoin address, otherwise it will inform you via the Command line.

## Example

1. **Select File**: Click the "Select File" button and choose a text file with Bitcoin addresses.
2. **Submit Addresses**: Click the "Submit Addresses" button to validate and query the addresses.
3. **Export Results**: Click the "Export Results" button to save the results to a CSV file.
