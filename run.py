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
    final_dict = {}
    xml_values= parse_xml_data_types("xml_values")  
    convert_dataframe_keys = parse_xml_data_types("convert_dataframe_keys") 
    # import pdb;pdb.set_trace()
    for i in  resp_str.split(xml_values["xml_obs_start"])[1:]:
        res = i.split(xml_values["xml_obs_end"])[0]
        for key in convert_dataframe_keys.keys():
            if convert_dataframe_keys[key] in final_dict:
                final_dict[convert_dataframe_keys[key]].append(str(res.split(key)[1].split("\"")[1]).strip())
            else:
                final_dict[convert_dataframe_keys[key]] = [str(res.split(key)[1].split("\"")[1]).strip()]
    return final_dict

def get_result_from_url(url, settings_dict):
    result = requests.get(url)
    resp_str = result._content.decode() 
    final_dict = None
    try:
        final_dict = extract_xml(resp_str, settings_dict)
    except Exception as e:
        print("Error occured while reading XML file error:"+str(e))

    dtype_dict= parse_xml_data_types("dtypes")  
    df = pd.DataFrame(final_dict)
    convert_df(df, dtype_dict)
    return df

def get_exchange_rate(source: str, target: str = "EUR") -> pd.DataFrame:

    settings_dict = read_setting_json("settings.json")
    url = settings_dict["url_start"]+source+settings_dict["url_sep"]+target+settings_dict["url_end"]
    df = get_result_from_url(url, settings_dict)
    return df

def get_raw_data(identifier: str) -> pd.DataFrame:
    settings_dict = read_setting_json("settings.json")
    url = settings_dict["raw_data_url_start"]+str(identifier)+settings_dict["raw_data_url_end"]
    df = get_result_from_url(url, settings_dict)
    return df

def merge_cols(first_df, seconddf, pkey="TIME_PERIOD", mul_val="OBS_VALUE"):
    if len(first_df)==1 or len(seconddf)==0:
        return pd.DataFrame()
    temp_df = first_df.merge(seconddf, on=pkey)
    first_df["OBS_VALUE"] = temp_df[mul_val+"_x"] * temp_df[mul_val+"_y"]
    return first_df

def get_data(identifier: str, target_currency: str = None) -> pd.DataFrame:
    raw_df = get_raw_data(identifier)
    if target_currency==None or len(target_currency.replace(" ",""))==0:
        return raw_df
    exchange_rate_df = get_exchange_rate(target_currency, identifier.split(".")[12])
    # exchange_rate_df = get_exchange_rate(target_currency)
    print(raw_df)
    print("exchange")
    print("*"*20)
    print(exchange_rate_df)
    return merge_cols(raw_df, exchange_rate_df)
 
# Driver program
if __name__ == "__main__":
    source_currency = input("Enter source currency: ")
    target_currency = input("Enter target currency or press return: ")

    source_identifier = "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N".split(".")
    source_identifier[12] = source_currency
    source_identifier = ".".join(source_identifier)

    df = get_data(source_identifier, target_currency)
    print(df)
    if len(df)==0:
        print("No data found")




