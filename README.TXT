Project: SABI Data Extraction, Management and model
Laura Cervera, Ivan Quirante and Joan Font

## Overview

This repository contains THREE main components:

With Visual studio core
1. dataExtraction: Automated scraping scripts using Selenium WebDriver to extract data from the SABI platform in batches.
2. DataManage: A set of Python scripts to clean, transform, and consolidate the raw data into a final analysis-ready CSV.
With Google Colab
3. model: The pythone notebook where we filtred the graph, displayed the plots and constructed the models

## Setup


1. Install Python dependencies:
   pip install -r requirements.txt

2. Store your SABI credentials securely. Create a config.py (not committed) with:
   USERNAME = "your\_username"
   PASSWORD = "your\_password"

## Usage

1. Data Extraction

   * Go to the dataExtraction folder.
   * Edit dataextraction.py:

     * Set driver\_path to your ChromeDriver path.
     * Update download\_dir to your desired downloads folder.
   * Run:
     python dataextraction.py
   * Check console output for download status. Raw Excel files will appear in download\_dir.

2. Data Management

   * Go to the DataManage folder. Ensure rawData contains downloaded .xls files.
   * Run scripts in this order: (some scripts might not work because change some data inside of the same folder so once it've been executed it does not have sense execute it again)
     python Script1.py   # Pivot and summarize per company
     python Script2.py   # Rename files by company ID
     python Script3.py   # Example pivot on single file (optional)
     python Script4.py   # Remove liquidated/dissolved companies
     python Script5.py   # Prune files missing records for 2000-2023
     python Script7.py   # Filter years >1998
     python Script8.py   # Add 'Empresa' column
     python Script9.py   # Impute missing values
     python Script10.py  # Concatenate into final\_data/all\_data.csv
   * After completion, find all\_data.csv in final\_data folder.

3. Model

   * Open google colab and launch the files

