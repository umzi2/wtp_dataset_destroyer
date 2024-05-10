from src.logic.process import ImgProcess
import json

with open('config.json') as f:
    config = json.load(f)

ImgProcess(config).run()
