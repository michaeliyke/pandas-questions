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
DOWNLOAD_PATH = Path("files")
BASE_URL = "https://stackoverflow.com"

QUESTIONS: List[Dict[str, Union[str, int, float, bool]]] = []
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
  global PAGES

  # We'll loop through the PAGES to get soup
  for soup in PAGES:
    questions_ = soup.find_all("div", class_="s-post-summary")

    for summary in questions_:
      question = summary.find("a", class_="s-link")
      stats = summary.find_all("div", class_="s-post-summary--stats-item")

      url_path = question.get("href")
      vote_count = stats[0].find(class_="s-post-summary--stats-item-number")

      answers_count = stats[1].find(class_="s-post-summary--stats-item-number")
      view_count = stats[2].find(class_="s-post-summary--stats-item-number")

      row = {
          "url_path": f"{url_path}",
          "question": f"{question.text.strip()}",
          "answers": answers_count.text.strip(),
          "views": view_count.text.strip(),
          "votes": vote_count.text.strip(),
          "best_answer": {},
      }

      QUESTIONS.append(row)

  PAGES = None
  return get_best_answer()


def sort_cb(answer: Dict[str, Union[str, int, bool]]) -> int:
  return answer["vote_count"]


def get_best_answer() -> Dict[str, Union[str, int, bool]]:
  answers: List[Dict[str, Union[str, int, bool]]] = []
  accepted_answer: Dict[str, Union[str, int, bool]]

  for row in QUESTIONS[:10]:
    url = f"{BASE_URL}{row['url_path']}"
    soup: bs4.BeautifulSoup = bs(requests.get(url).text, "html.parser")

    save(f"files/pages/{name_file()}.html", str(soup))
    post: bs4.element.Tag

    for post in soup.select("div.post-layout"):
      text = post.select_one("div.s-prose p:first-of-type").text.strip()

      vote_count = post.select_one("div.js-vote-count").text.strip()
      accepted_: bs4.Tag = post.select_one("div[aria-label='Accepted']")
      answer: Dict[str, Union[str, int, bool]] = {}

      answer["text"] = text
      answer["vote_count"] = vote_count
      answer["accepted"] = False

      # If accepted_ is hidden, then it's not the accepted answer
      if (accepted_ and "d-none" not in accepted_.get("class")):
        answer["accepted"] = True

        accepted_answer = answer
      answers.append(answer)

    time.sleep(60)

  save("files/answers-data.json", json.dumps(answers, indent=2))
  answers.sort(key=sort_cb)
  most_voted = answers.pop()

  if(accepted_answer["text"] == ""):
    accepted_answer = most_voted

  row["accepted_answer"] = accepted_answer


extract_data()
save("files/questions-data.json", json.dumps(QUESTIONS, indent=2))
