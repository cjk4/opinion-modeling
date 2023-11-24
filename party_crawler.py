from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
import re
import json
import random

def split_twitter_handle(handle):
  if handle.islower():
    return handle + '>>>>>>>>>>>>'
  words = re.findall('[A-Z][a-z]*', handle)
  return ' '.join(words) if words else handle

def find_sequence(text):
    match = re.search(r'([A-Z])-([A-Z][A-Z])', text)
    if match:
        return match.group(1)
    else:
        return None
    
def find_sequence_2(text):
    if 'democrat' in text.lower() or 'democratic' in text.lower():
        return 'D'
    elif 'republican' in text.lower():
        return 'R'
    else:
        return None

def crawl_twitter_handles(handles):
  chromedriver_autoinstaller.install()
  chrome_options = Options()
  chrome_options.add_argument("--blink-settings=imagesEnabled=false")

  driver = webdriver.Chrome(options=chrome_options)

  results = []
  try:
    for handle in handles:
      search_query = f"{handle}"
      driver.get(f"https://www.google.com/search?q={search_query}")

      try:
        anchor_tag = driver.find_element(By.CLASS_NAME, 'xGj8Mb')
        text_content = anchor_tag.text
        href_attribute = anchor_tag.get_attribute("href")
        party = find_sequence(text_content)
        if party is None:
            party = find_sequence_2(text_content)
      except:
        party = ''
        href_attribute = ''

      print(f"Handle: {handle}")
      print(f"Party: {party}")
      # print(f"Text Content: {text_content}")
      # print(f"Href Attribute: {href_attribute}")
      results.append({
        'handle': handle,
        'party': party,
      })
      
      time.sleep(random.randint(1, 3))

  finally:
    # Close the browser window
    driver.quit()

  return results


with open('data/split_handles_final.txt', 'r') as file:
  split_handles = file.read().splitlines()

print(split_handles)

parties = crawl_twitter_handles(split_handles)

with open('data/parties_2.json', 'w') as file:
  json.dump(parties, file, indent=2)
