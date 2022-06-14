"""
This script provides a subset of the command line arguments for processing
county level climate data from NOAA NCEI FTP site.
"""
import os
import argparse
import pandas as pd
import requests

def main():
    """ Sends request to the Quick Stats API and aggregates data by county and year

    Parameters
    ----------
    None

    Returns
    ---------
    csv file
        data summarized by county and year
        and monthly values
    """
   
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-s", "--source", help= "input text file", type=str)
    parser.add_argument("-p", "--path", help= "path to input file", type=str)
    parser.add_argument("-o", "--outpath", help= "path to input file", type=str)


    args = parser.parse_args()

    source = args.source
    path = args.path
    outpath = args.outpath

    #'\s+' as delimiter or delim_whitespace=True will work
    # dtype = str to maintain leading 0 in 1st column
    data = pd.read_csv(os.path.join(path, source), header = None, delim_whitespace=True, dtype = str)

    for col in data.columns:
        if col == 0:
            data[col] = data[col].astype('str')
        if col !=0:
            data[col]= pd.to_numeric(data[col])
        
    data = data.rename(columns={0:"code", 1:"Jan", 2:"Feb",3:"Mar", 4:"Apr", 5:"May",
                                6:"Jun", 7:"Jul", 8:"Aug",
                                9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"})

    data['Year'] = data["code"].apply(lambda x: x[-4:])
    data['st_code'] = data["code"].apply(lambda x: x[:2])
    data['fips_code5'] = data["code"].apply(lambda x: x[:5])

    fips = pd.read_csv('C:/Projects/CSIS638/Project/data/FIPS/national_county.txt', header = None, delimiter=",", dtype = str)
    fips = fips.rename(columns={0:"State", 1:"st_code", 2:"fips3",3:"County"})
    fips["fips_code5"] = fips['st_code']+ fips["fips3"]
    fips = fips.drop(columns=[4])

    data_final = pd.merge(data, fips, on="fips_code5")
    data_final = data_final.drop(columns=["code", "st_code_x", "st_code_y", "fips3", "fips_code5"])

    data_final = data_final[["State", "County", "Year", "Jan", "Feb", 
                            "Mar", "Apr", "May", "Jun", "Jul", "Aug", 
                            "Sep", "Oct", "Nov", "Dec"]]

    os.makedirs(outpath, exist_ok=True)
    out_file = source.replace('-v1.0.0-20220607','')
    
    return data_final.to_csv(os.path.join(outpath,f"{out_file}.csv"))
    
if __name__ == "__main__":
    main()
    