#1. import required packages and modules
#=======================================
import json as json
import datetime as dt
import scrapper as scraper
from typing import Iterator


#2. specifies the date range we want to fetch events for
#=======================================================
def date_range(start_date: dt.date, end_date: dt.date) -> Iterator[dt.date]:
    for n in range(int((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)


#3. get events and store them in a dictionary
#============================================
def create_events_dict():
    events = dict()
    start_date = dt.date(2020, 1, 1)
    end_date = dt.date(2020, 1, 5)

    for date in date_range(start_date, end_date):
        month = date.strftime("%B").lower() #3.1 dont get the month as a number
        if month not in events:
            #3.2 create the month as an empty dict if its not there
            events[month] = dict()

        events[month][date.day] = scraper.events_of_the_day(month, date.day)

    return events


#4. store the scrapped events to events.json
#===========================================
if __name__ == "__main__":
    events = create_events_dict()
    with open("events.json", mode="w") as events_file:
        json.dump(events, events_file, ensure_ascii=False)