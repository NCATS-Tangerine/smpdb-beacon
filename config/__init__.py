import os
import yaml

from yaml import FullLoader

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')

with open(path, 'r') as f:
    config = yaml.load(f, Loader=FullLoader)
