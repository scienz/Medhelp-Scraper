from pathlib import Path
import os

def create_dir(name: str):
    path = _build_path(name)
    os.umask(000)
    os.makedirs(path, mode = 0o777, exist_ok = True)

def create_file(name: str, content):
    path = _build_path(name)
    if (type(content) is str):
        with open(path, 'w', encoding = "utf-8") as f:
            f.write(content)
    else:
        with open(path, 'wb') as f:
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

def normalize_path_name(name):
    chars = '\/:*?"<>|\''
    for c in chars:
        name = name.replace(c, '')
    return name

def _build_path(name):
    return Path.cwd() / Path(name)
