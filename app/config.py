import os
import json
CONFIG_NAME = "config.json"
dir = os.path.dirname(os.path.dirname(__file__))
abs_file = os.path.join(dir, CONFIG_NAME)



DEFAULT_CONFIG = {
    "resolution":"640x480",
    "rotation":0,
    "framerate":24,
}

def load():
    configuration = None
    if os.path.exists(abs_file):
        with open(abs_file) as f:
            configuration = json.load(f)
    else:
        # if the config does not exist
        configuration = DEFAULT_CONFIG
    return configuration



def save(configuration):
    with open(abs_file) as f:
        json.dump(f,configuration, indent=2)