import pandas as pd
import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

def Authentication():
    header = {
        "Content-Type" : "application/json"
    }
    json_data = {
        "apiKey" : os.environ.get("apiKey_CJ_dropshipping")
    }
    response = requests.post("https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken",headers=header,json = json_data)
    return(response)

def Save_Credentials(response):
    with open ("Credentials.json","w") as f:
        Credentials = response.json()
        json.dump(Credentials,f,indent=4)
    return()

# response = Authentication()
# Save_Credentials(response)

def Get_Data():
    current_page = 1
    total_page = 1
    Master_Data = []

    headers = {
        "CJ-Access-Token" : os.environ.get("CJ_Access_Token")
    }

    params = {
        "KeyWord" : "Laptop",
        "Size" : 20,
        "page" : current_page
    }

    while current_page<=total_page:
        try:
            response = requests.get("https://developers.cjdropshipping.com/api2.0/v1/product/listV2",headers=headers,params=params)
        except Exception as e:
            print(f"Error Occured of the type | {e}")
            exit()
        Data = response.json()
        if current_page == 1:
            total_page = Data["data"]["totalPages"]
            print(f"Number of pages : {total_page}")
        current_page+=1
        params["page"] = current_page
        for value in Data["data"]["content"][0]["productList"]:
            entry = {
                "id" : value.get("id","Not Found"),
                "name" : value.get("nameEn","Not Found"),
                "image" : value.get("bigImage","Not Found"),
                "Selling-Price" : value.get("sellPrice","Not Found")
            }
            Master_Data.append(entry)
        print("Extraction successful")
        time.sleep(1)
    return(Master_Data)

Master_Data = Get_Data()

def Save_Data(Master_Data):
    with open ("Data.json","w") as f:
        json.dump(Master_Data,f,indent=4)
    return()

# Save_Data(Master_Data)

def Make_CSV(Master_Data):
    entry = pd.DataFrame(Master_Data)
    entry["Selling-Price-min"] = entry["Selling-Price"].str.split(" -- ").str[0]
    entry["Selling-Price-max"] = entry["Selling-Price"].str.split(" -- ").str[1]
    entry["Selling-Price-max"] = entry["Selling-Price-max"].fillna(entry["Selling-Price-min"])
    entry = entry.drop(["Selling-Price"],axis=1)
    entry["Selling-Price-min"] = pd.to_numeric(entry["Selling-Price-min"])
    entry["Selling-Price-max"] = pd.to_numeric(entry["Selling-Price-max"])
    entry["Average-Selling-Price"] = (entry["Selling-Price-min"] + entry["Selling-Price-max"])/2.0
    average = entry["Average-Selling-Price"].mean()
    print(average)
    entry = entry[entry["Average-Selling-Price"] < (0.8 * average)]
    entry = entry.sort_values(["Average-Selling-Price"],ascending=False)
    entry.to_csv("retailer_product_extractor.csv",index=False)
    print("retailer_product_extractor.csv created SUCCESSFULLY")
    return()

Make_CSV(Master_Data)
