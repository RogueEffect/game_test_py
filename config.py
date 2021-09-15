
import json
import os


class Config:
    """Class that holds various config values"""
    def __init__(self, path='config.json'):
        self.basepath = os.getcwd()
        self.load_config(path)
    
    def load_config(self, path):
        with open(path, encoding='utf-8') as f:
            obj = json.load(f)
        for key, value in obj.items():
            setattr(self, key, value)
