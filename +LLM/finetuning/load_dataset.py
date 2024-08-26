import json


def read_ds_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data
