import json
from directory_manager import get_fp

def save_as_json(dct, path):
    print("Saving " + path + " ...")
    with get_fp(path, 'w') as fp:
        json.dump(dct, fp, indent=2)
