from configparser import ConfigParser

def parse_xml_data_types(sec_name):
    config_parser = ConfigParser()
    config_parser.optionxform=str
    config_parser.read("xml.config")
    var_type_dict = {}
    final_dtype={}
    for section_name in config_parser.sections():
        if section_name == sec_name:
            for index in config_parser.items(section_name):
                if sec_name=="dtypes":
                    var_type_dict[index[0]] = index[1].split(",")
                    for i in var_type_dict[index[0]]:
                        if index[0]=="string":
                            final_dtype[i]=str
                        else:
                            final_dtype[i]=float
                else:
                    final_dtype[index[0]]=index[1]
    return final_dtype