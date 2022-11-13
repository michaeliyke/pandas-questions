"""Load all downloaded files and extract data: JSON and """

import csv
import json
import bs4
import time
import requests
from bs4 import BeautifulSoup as bs
from typing import List, Dict, Union
from pathlib import Path
from personal.setup import name_local_file as name_file, save_file as save


PAGES: List[bs4.element.Tag] = []
DOWNLOAD_PATH = Path("files/pages")
BASE_URL = "https://stackoverflow.com"

ROWS: List[Dict[str, Union[str, int, float, bool]]] = []
CSV_HEADERS: List[str] = []

# LOAD PAGE FILES
for _path in DOWNLOAD_PATH.iterdir():
  if _path.suffix != ".html":
    continue

  time.sleep(0.5)

  with open(_path.resolve(), "r", encoding="UTF-8") as _file:
    PAGES.append(bs(_file.read(), "html.parser"))
    print(_file.name, "has been loaded!")
print("ALL FILES LOADED!")


def extract_data():
  """Function to scrape a single page"""
  questions = []
  global PAGES

  # We'll loop through the PAGES to get soup
  for soup in PAGES:
    questions_ = soup.find_all("div", class_="s-post-summary")

    for summary in questions_:
      question = summary.find("a", class_="s-link").text
      stats = summary.find_all("div", class_="s-post-summary--stats-item")
      url_path = question.get("href")

      vote_count = stats[0].find(
          class_="s-post-summary--stats-item-number").text

      answers_count = stats[1].find(
          class_="s-post-summary--stats-item-number").text

      view_count = stats[2].find(
          class_="s-post-summary--stats-item-number").text

      row = {
          "url_path": f"{url_path}",
          "question": f"{question}",
          "answers": f"{answers_count}",
          "views": f"{view_count}",
          "votes": f"{vote_count}",
          "best_answer": {},
      }

      questions.append(row)

  if(not questions):
    raise Exception("Data does not exist")

  PAGES = None
  ROWS.extend(questions)

  return get_best_answer()


def sort_cb(answer: Dict[str, Union[str, int, bool]]) -> int:
  return answer["vote_count"]


def get_best_answer() -> Dict[str, Union[str, int, bool]]:
  answers: List[Dict[str, Union[str, int, bool]]] = []
  accepted_answer: Dict[str, Union[str, int, bool]]

  for row in ROWS:
    url = f"{BASE_URL}{row['url_path']}"
    time.sleep(2)
    soup: bs4.BeautifulSoup = bs(requests.get(url).text, "html.parser")
    save(f"files\pages\{name_file()}.html")
    post: bs4.element.Tag

    for post in soup.select("div.post-layout"):
      text = post.select_one("div.s-prose p:first-of-type").text.strip()

      vote_count = post.select_one("div.js-vote-count").text.strip()
      accepted_: bs4.Tag = post.select_one("div[aria-label='Accepted']")
      answer: Dict[str, Union[str, int, bool]] = {}

      answer["text"] = text
      answer["vote_count"] = int(vote_count)
      answer["accepted"] = False

      # If accepted_ is hidden, then it's not the accepted answer
      if ("d-none" not in accepted_.get("class")):
        answer["accepted"] = True
        accepted_answer = answer

      answers.append(answer)

  answers.sort(key=sort_cb)
  most_voted = answers.pop()

  if(accepted_answer["text"] == ""):
    accepted_answer = most_voted

  return accepted_answer


extract_data()
