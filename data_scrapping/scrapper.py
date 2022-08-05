#1. import required packages and modules
#=======================================
import bs4 as bs4
from typing import List
import requests as requests


#2. generate the url and return it
#=================================
def generate_month_url(month: str, day: int) -> str:
    url = f"https://www.onthisday.com/day/{month}/{day}"
    return url

#3. get the page and return a beautiful soup object
#==================================================
def get_page(url: str) -> bs4.BeautifulSoup:
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    return soup

#4. get events of the specified day and return them as a list of strings
#=======================================================================
def events_of_the_day(month: str, day: int) -> List[str]:
    url = generate_month_url(month, day)
    page = get_page(url)
    raw_events = page.find_all(class_="event")
    events = [event.text for event in raw_events]
    return events

