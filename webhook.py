import requests
import os
from dotenv import load_dotenv

load_dotenv()
file_path = "D:/scripts/retailer_product_extractor.csv"
with open (file_path,"rb") as f:
    my_payload_file = {
    "files" : (file_path,f,"text/csv")
    }
    my_payload_heading = {
    "header" : "retailer_product_details"
    }
    try:
        requests.post(os.environ.get("n8n_web_hook_URL"),files=my_payload_file,json=my_payload_heading)    
        print("Data Transferred Successfully")
    except Exception as e:
        print(f"Error Occured | Error : {e}")

