from src.logic.process import ImgProcess
import argparse
import re
import hcl2


def number_fix(string_object):
    match_re = re.search(r"\$\{(-?\d*\.\d+|-?\d+)\}", string_object)
    if match_re:
        number_str = match_re.group(1)
        if "." in number_str:
            return float(number_str)
        else:
            return int(number_str)
    return string_object


def list_search(no_detect_list):
    for index in range(len(no_detect_list)):
        list_object = no_detect_list[index]
        if isinstance(list_object, str):
            no_detect_list[index] = number_fix(list_object)
        elif isinstance(list_object, dict):
            no_detect_list[index] = fix_hcl_dict(list_object)
        elif isinstance(list_object, list):
            no_detect_list[index] = list_search(list_object)
    return no_detect_list


def fix_hcl_dict(dict_hcl):
    for key in dict_hcl.keys():
        object = dict_hcl[key]
        if isinstance(object, str):
            dict_hcl[key] = number_fix(object)
        elif isinstance(object, list):
            dict_hcl[key] = list_search(object)
        elif isinstance(object, dict):
            dict_hcl[key] = fix_hcl_dict(object)
    return dict_hcl


parser = argparse.ArgumentParser(
    prog="Wtp Dataset Destroyer",
    description="Mini framework for creating paired datasets.",
)
parser.add_argument(
    "-f",
    "--folder",
    default="configs/default.json",
    help="Path to your config. Default = configs/default.json",
)
json_folder = parser.parse_args().folder
with open(json_folder) as file:
    config = hcl2.load(file)
config = fix_hcl_dict(config)
# ImgProcess(config)
ImgProcess(config).run()
