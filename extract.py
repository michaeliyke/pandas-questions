"""Load all downloaded files and extract data: JSON and """

import csv
import json
import random
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

print("\nLOADING PAGE FILES")
for _path in DOWNLOAD_PATH.iterdir():
  if _path.suffix != ".html":
    continue

  time.sleep(0.5)

  with open(_path.resolve(), "r", encoding="UTF-8") as _file:
    PAGES.append(bs(_file.read(), "html.parser"))
    print(_file.name, "has been loaded!")
print("SUCCESSFUL!\n")


def extract_data():
  """Function to scrape a single page"""
  global PAGES

  # We'll loop through the PAGES to get soup
  print("\nLOADING QUESTIONS TO MEMORY")
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

  print("SUCCESSFUL!\n")
  PAGES = None
  return get_best_answer()


def sort_cb(answer: Dict[str, Union[str, int, bool]]) -> int:
  return answer["vote_count"]


def get_best_answer() -> Dict[str, Union[str, int, bool]]:
  answers: List[Dict[str, Union[str, int, bool]]] = []
  accepted_answer: Dict[str, Union[str, int, bool]]

  print("\nGETTING: BEST ANSWER FOR QUESTION")
  # for question in QUESTIONS[:10]:
  for question in QUESTIONS:
    url = f"{BASE_URL}{question['url_path']}"
    time.sleep(10 + random.randrange(10, 61, random.randrange(1, 10, 2)))

    soup: bs4.BeautifulSoup = bs(requests.get(url).text, "html.parser")
    save(f"files/pages/{name_file()}.html", str(soup))

    post: bs4.element.Tag
    for post in soup.select("div.post-layout"):
      text_o = post.select_one("div.s-prose p:first-of-type")

      text = text_o.text.strip() if(text_o) else ""
      vote_count_o = post.select_one("div.js-vote-count")
      vote_count = vote_count_o.text.strip() if(vote_count_o) else "0"

      accepted_: bs4.Tag = post.select_one("div[aria-label='Accepted']")
      answer: Dict[str, Union[str, int, bool]] = {}

      answer["text"] = text
      answer["vote_count"] = vote_count
      answer["accepted"] = False
      answer["question"] = question["question"]

      # If accepted_ is hidden, then it's not the accepted answer
      if (accepted_ and "d-none" not in accepted_.get("class")):
        answer["accepted"] = True
        accepted_answer = answer

      answers.append(answer)

  print("SUCCESSFUL!\n")
  save("files/answers-data.json", json.dumps(answers, indent=2))

  answers.sort(key=sort_cb)
  most_voted = answers.pop()

  if(accepted_answer["text"] == ""):
    accepted_answer = most_voted

  question["best_answer"] = accepted_answer


extract_data()
save("files/questions-data.json", json.dumps(QUESTIONS, indent=2))

print("ALL DONE!!!")
