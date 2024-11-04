"""
2024 File Classifier
"""
import glob
import os
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


if __name__ == "__main__":
    origin_path = os.getenv("ORIGIN_DIRECTORY")
    destiny_path = os.getenv("DESTINY_DIRECTORY")
    file_classifier(origin_path, destiny_path, mode="copy")
