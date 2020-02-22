from pathlib import Path
import os

def createDir(name: str):
    path = _build_path(name)
    os.umask(000)
    os.makedirs(path, mode = 0o777, exist_ok = True)

def create_file(name: str, content):
    path = _build_path(name)
    try:
        with open(path, 'wb', encoding = "utf-8") as f:
            f.write(content)
    except:
        with open(path, 'w', encoding = "utf-8") as f:
            f.write(content)

def file_exists(name: str):
    path = _build_path(name)
    return path.exists()

def read_file(name: str, mode):
    try:
        path = _build_path(name)
        with open(path, mode) as f:
            return f.read().decode() if mode == 'rb' else f.read()
    except:
        pass

def get_fp(name, mode):
    path = _build_path(name)
    return open(path, mode)

def _build_path(name):
    return Path.cwd() / Path(name)
