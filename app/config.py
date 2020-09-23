import os
import json
CONFIG_NAME = "config.json"
dir = os.path.dirname(os.path.dirname(__file__))
abs_file = os.path.join(dir, CONFIG_NAME)
config = None

if os.path.exists(abs_file):
    with open(abs_file) as f:
        config = json.load(f)


print(config)
