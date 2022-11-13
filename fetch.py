import requests, time
from personal.setup import name_local_file as name_file, save_file as save

URL = "https://stackoverflow.com/questions/tagged/pandas"
PAGE_LIMIT = 2


def build_url(base_url=URL, tab="frequent", page=1):
  """Build URL for a page: 
    eg  https://stackoverflow.com/questions/tagged/pandas?tab=frequent&page=2
  """
  return f"{base_url}?tab={tab}&page={page}"


def save_page(page=1):
  """Function to save a single page to disk"""
  time.sleep(2)
  response = requests.get(build_url(page=page))

  file_name = "{}.html".format(name_file())
  save(file_name, response.text)
  print(file_name, "saved!")


def initiate():
  """Function to page download/save to PAGE_LIMIT"""
  print("Starting page download!")
  
  for i in range(1, PAGE_LIMIT + 1):
    save_page(page=i)
  
  print("Download completed!")


if __name__ == "__main__":
  initiate()