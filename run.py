import pandas as pd 
import requests
import json

def read_setting_json(file_name: str)-> dict:
    with open(file_name, 'r') as file:
        return json.load(file)
def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:

    settings_dict = read_setting_json("settings.json")
    url = settings_dict["url_start"]+source+settings_dict["url_sep"]+target+settings_dict["url_end"]
    result = requests.get(url)
    resp_str = result._content.decode() 
    file = open("result.xml","w") 
    file.write(str(resp_str))
    final_dict = {"ObsDimension":[],"ObsValue":[]}
    for i in  resp_str.split(settings_dict["xml_obs_start"])[1:]:
        res = i.split(settings_dict["xml_obs_end"])[0]
        for keys in final_dict.keys():
            
        print(res)
        print("*"*20)
    # import pdb;pdb.set_trace()

get_exchange_rate("GBP")

