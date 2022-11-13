import os
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Edge
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions

from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager as EdgeDriverManager
from selenium.webdriver.common.by import By
import json
from pathlib import Path

# IN-MEMORY for now
LOCAL_FILES_STORE = []


def cls():
    os.system("cls")
    return None


def name_local_file(initial_name=""):
    time_str = str(time.time()).replace(".", "")

    if not initial_name:
        return "{}.txt".format(time_str)

    else:
        p = Path(initial_name)
        temp = str(p.resolve()).replace(".{}".format(p.suffix), "")
        return "{}-{}.{}".format(temp, time_str, p.suffix)


def save_file(file_name: str, content: str):
    """save file locally if not saved"""

    if not file_name:
        raise ValueError("save_file: file name required")

    if not file_name.startswith("files/"):
        file_name = "files/{}".format(file_name)

    if file_name in LOCAL_FILES_STORE:
        return

    with open(file_name, "w") as f:
        f.write(content)

    LOCAL_FILES_STORE.append(file_name)
    print("{} has been saved".format(file_name))


def load_file(fn):
    with open(fn, "r") as f:
        content = f.read()
    return content


def get_cookies(file_name):
    file_path = Path(file_name)

    with open(file_path.absolute(), "r", encoding="UTF-8") as f:
        data = f.read()

        dict_ = json.loads(data)
        return dict_["cookies"]


def trim_cookie(cookie):
    allowed = ["name", "domain", "value"]

    for key, _ in list(cookie.items()):
        if not key in allowed and key in cookie:
            del cookie[key]

    return cookie


def transform_cookies(cookies):

    for cookie in cookies:
        if cookie["domain"].startswith("."):
            cookie["domain"] = cookie["domain"][1:]

        # trim_cookie(cookie)
    return cookies


def add_cookies(cookies, driver):
    for cookie in cookies:
        driver.add_cookie(cookie)


# __all__ = [
#   get_cookies, trim_cookie, transform_cookies, add_cookies,
#   bs, Edge, EdgeOptions, EdgeService, EdgeDriverManager, By,
#   options, service, edge_driver_manager,
# ]
