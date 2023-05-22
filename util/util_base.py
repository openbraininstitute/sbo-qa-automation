import os
import json


def load_config():
    try:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        config_path = os.path.join(base_dir, '..', 'util', 'config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return \
            None


def load_links():
    with open('links.json', 'r') as file:
        links = json.load(file)
    return links
