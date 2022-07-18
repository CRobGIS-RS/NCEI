#NCEI 
This repository contains Python code for processing county level climate data downloaded from the climdiv ftp site. This was developed to support my class project for CSIS638 Implementation of Database Management Systems.

##noaa_cnty_climate_data.py

In 2019, the National Oceanic Atmospheric Administration (NOAA) National Centers for Environmental Information (NCEI) began providing county-level data on Temperature and Precipitation. These data are generated from a dataset called nClimGrid which is derived from a network of historical climate data. To access the historical data dating back to 1895, text files containing the information can be downloaded from FTP (ftp://ftp.ncdc.noaa.gov/pub/data/cirs/climdiv/). 

This script was used to process data on the following climate variables:
*Precipitation
*Average Temperature
*Cooling Degree Days
*Maximum Temperature
*Minimum Temperature

The data offered through FTP was formatted slightly differently than NCEI’s other offerings. State, county, and year information for each record were concatenated into a single code and no headings were provided. The states and counties were represented as numeric codes based on the Federal Information Processing Standards (FIPS) system. To format the data, the CSV files were read into a Pandas dataframe and the heading code elements were parsed. To attach the actual state and county name associated with each record the dataframe with the climate observations was joined to another dataframe containing FIPS codes and their accompanying state and county names. The schema of the final dataframe was reorganized and exported as a CSV file for later ingestion into a MySQL database. T

##load_csv_tables_mysql.py
The data acquisition process resulted in having 5 CSV files that need to be ingested into the MySQL database as a set of tables. Climate data was organized by variable (ex. Precipitation) with each containing observations for every county from 1997-2021. The process for ingesting the climate data relied mainly on the Pandas and MySQL Connector for Python packages. MySQL Connector made it possible to insert a connection to the database into the scripts as well as submit SQL commands using a Cursor. Each climate CSV file was read into a Pandas dataframe. Then a table was created for each climate variable and a schema was declared using the CREATE TABLE command in SQL. Each record of the climate dataframes was converted into a tuple and added to the database table using the INSERT INTO command. 
