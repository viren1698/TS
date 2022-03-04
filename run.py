import pandas as pd 
import requests
import json
from util import parse_xml_data_types

def read_setting_json(file_name: str)-> dict:
    with open(file_name, 'r') as file:
        return json.load(file)

def convert_df(df, dtype_dict):
    for i in dtype_dict:
        if i in df:
            if dtype_dict[i] ==float or dtype_dict[i] ==int:
                df[i] = pd.to_numeric(df[i])
            elif dtype_dict[i] =="datetime":
                df[i] = pd.to_datetime(df[i])   

def extract_xml(resp_str: str, settings_dict: dict) ->dict:
    final_dict = {"ObsDimension":[],"ObsValue":[]}
    for i in  resp_str.split(settings_dict["xml_obs_start"])[1:]:
        res = i.split(settings_dict["xml_obs_end"])[0]
        for key in final_dict.keys():
            final_dict[key].append(res.split(key)[1].split("\"")[1])
    return final_dict

def get_result_from_url(url, settings_dict):
    result = requests.get(url)
    resp_str = result._content.decode() 
    # file = open("result.xml","w") 
    # file.write(str(resp_str))

    final_dict = extract_xml(resp_str, settings_dict)

    dtype_dict= parse_xml_data_types("dtypes")  
    df = pd.DataFrame(final_dict)
    convert_df(df, dtype_dict)
    return df

def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:

    settings_dict = read_setting_json("settings.json")
    url = settings_dict["url_start"]+source+settings_dict["url_sep"]+target+settings_dict["url_end"]
    df = get_result_from_url(url, settings_dict)
    

    print(df)
    return df

def get_raw_data(identifier: str) -> pd.DataFrame:
    settings_dict = read_setting_json("settings.json")
    url = settings_dict["raw_data_url_start"]+str(identifier)+settings_dict["raw_data_url_end"]
    df = get_result_from_url(url, settings_dict)
    print(df)
    return df


# get_exchange_rate("GBP")
# get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")

