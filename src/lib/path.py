from pathlib import Path
from typing import List
import os


def get_files(folder: str):
    result: List[str] = []
    test_path = Path(os.getcwd()).joinpath(folder).resolve()

    for root, _, files in os.walk(test_path, topdown=False):
        for name in files:
            if name.endswith('.js'):
                result.append(os.path.join(root, name))

    return result
