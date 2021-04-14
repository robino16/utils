"""
# App Config Template
by robinoms
"""

import os
import logging
import json

CONFIG_FILE = 'app.conf'
CONFIG_LOAD = False  
CONFIG_SAVE = False

BANNED = '<banned>'


class AppConfig:
    def __init__(self, json_dict: None) -> None:
        self.data_folder = 'data/'
        self.output_folder = 'output/'

        # logger module
        self.log_format = '[%(asctime)s] - %(filename)-30s - line %(lineno)-5d - %(levelname)-8s - %(message)s'
        self.log_output_file = self.output_folder + 'app.log'
        self.log_level = logging.INFO

        if json_dict:
            vars(self).update(json_dict)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def save_app_config(path: str, config: AppConfig):
    with open(path, 'w') as file:
        file.write(config.to_json())


def load_app_config(path):
    if CONFIG_LOAD and os.path.isfile(path):
        config = json.loads(open(path, 'r').read(), object_hook=AppConfig)
    else:
        config = AppConfig()
        if CONFIG_SAVE:
            save_app_config(config)
    return config


conf = load_app_config()
logging.basicConfig(level=conf.log_level,
                    format=conf.log_format,

                    # uses two handlers:
                    #     1. to file
                    #     2. terminal output

                    handlers=[logging.FileHandler(conf.log_output_file), logging.StreamHandler()])
log = logging.getLogger()
