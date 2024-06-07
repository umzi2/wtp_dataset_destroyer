from src.logic.process import ImgProcess
import json
import argparse

parser = argparse.ArgumentParser(
    prog='Wtp Dataset Destroyer',
    description='Mini framework for creating paired datasets.')
parser.add_argument('-f', '--folder',
                    default="configs/default.json", help="Path to your config. Default = configs/default.json")
json_folder = parser.parse_args().folder
with open(json_folder) as f:
    config = json.load(f)

ImgProcess(config).run()
