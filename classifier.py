"""
2024 File Classifier
"""
import glob
import os
import platform
import re
import shutil
import logging
import sys
from typing import Tuple

stdout_handler = logging.StreamHandler(stream=sys.stdout)
logging.basicConfig(format="%(asctime)s %(module)s %(funcName)s %(process)d [%(levelname)s]: %(message)s",
                    level=logging.INFO,
                    handlers=[stdout_handler])
_logger = logging.getLogger()


def file_classifier(origin_dir, destiny_dir, mode="copy") -> Tuple[list, list]:
    """
    Copy or move files from source folder to specific folder/extension
    This function categorize each of the files automatically
    :param origin_dir: source folder to scan files
    :param destiny_dir: destination of the files
    :param mode: copy or move
    :return: Tuple[scan_files, copied_files]
    """
    scanned_files = [f for f in glob.glob(origin_dir + "/*.*") if os.path.isfile(f)]
    copied_files = list()
    if not os.path.exists(destiny_dir):
        os.mkdir(destiny_dir)
    for file in scanned_files:
        try:
            ext = re.search(r"[0-9a-zA-Z]+$", file).group().lower()
            if not ext:
                continue
            dir_path = f"{destiny_dir}/{ext}"
            if not os.path.exists(dir_path):
                os.mkdir(f"{destiny_dir}/{ext}")
            getattr(shutil, mode)(file, dir_path)
            _logger.info(f"File {file} move to {dir_path}")
        except FileNotFoundError as ex:
            _logger.error(f"File {file}, could not be move, error: {ex}")
        except OSError as ex:
            _logger.error(f"File {file}, could not be open, error: {ex}")
        except Exception as ex:
            _logger.error(f"File {file} got Unknown error: {ex}")
        else:
            copied_files.append(file)
    _logger.info(f"Files copied: {len(copied_files)}/{len(scanned_files)}")
    return scanned_files, copied_files


def get_default_path():
    """
    Get default path depending on the current OS
    :return: _default - str
    """
    if "Windows" in platform.platform():
        _default = f"C:{os.getenv('HOMEPATH')}/Downloads"  # Intended for Windows OS
    elif "Linux" in platform.platform():
        _default = os.getenv("HOME")  # Intended for Linux OS
    else:
        _default = ""
    return _default


def run():
    """
    Run program
    Setting environment variables ORIGIN_DIRECTORY, DESTINY_DIRECTORY will overwrite any paths obtain as an input from
    the user.
    """
    while True:
        _default = get_default_path()
        _origin = input(f"Introduce origin path to start file classification, default {_default}: ") or _default
        _logger.info(f"Path to manage files {_origin}")
        _destination = input("Add destination path to store files by file extension: ") or f"{_default}/classifier"
        _logger.info(f"Path to destination folder {_destination}")
        _mode = input("Select which mode to use:\n1) Copy\n2) Move\n")

        origin_path = os.getenv("ORIGIN_DIRECTORY", _origin)
        destiny_path = os.getenv("DESTINY_DIRECTORY", _destination)
        file_classifier(origin_path, destiny_path, mode={"1": "copy", "2": "move"}.get(_mode, "1"))
        running = input("Start new classifier process:\n1) Yes\n2) No\n")
        if running != "1":
            _logger.info("Exiting program")
            break


if __name__ == "__main__":
    run()
