import json
from directory_manager import get_fp
from pathlib import PurePath

def save_as_json(dct, path):
    try:
        print("Saving " + path + " ...")
        with get_fp(PurePath(path), 'w') as fp:
            json.dump(dct, fp, indent=2)
    except Exception as e:
        print(e)
        pass
