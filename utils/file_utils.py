
import os
from typing import List


def get_all_files(directory: str, extensions: List[str]) -> List[str]:
    files = []
    for filename in os.listdir(directory):
        if any(filename.lower().endswith(ext) for ext in extensions):
            files.append(os.path.join(directory, filename))
    return files


def ensure_dir(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

