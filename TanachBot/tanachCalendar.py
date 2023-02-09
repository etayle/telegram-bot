from datetime import datetime, timedelta, date
from cal_setup import get_calendar_service
import tanachParser
import re

def main():
   # creates one hour event tomorrow 10 AM IST
   service = get_calendar_service()

   d = datetime.now().date()
   tomorrow = datetime(d.year, d.month, d.day, 10)+timedelta(days=1)
   start = tomorrow.isoformat()
   end = (tomorrow + timedelta(hours=1)).isoformat()
   start_date = date(2023, 3, 21)
   end_date = date(2023, 10, 7)
   for single_date in tanachParser.daterange(start_date, end_date):
        text = tanachParser.getSeder(single_date)
        if text == None:
            continue
        start = datetime(single_date.year, single_date.month, single_date.day, 10)
        end = (start + timedelta(hours=1)).isoformat()
        event_result = service.events().insert(calendarId='primary',
            body={
                "summary": re.search('<b>(.*)</b>',text.split(",")[0]).group(1),
                "description": text,
                "start": {"dateTime": start.isoformat(), "timeZone": 'Israel'},
                "end": {"dateTime": end , "timeZone": 'Israel'},
            }
        ).execute()

#    print("created event")
#    print("id: ", event_result['id'])
#    print("summary: ", event_result['summary'])
#    print("starts at: ", event_result['start']['dateTime'])
#    print("ends at: ", event_result['end']['dateTime'])

if __name__ == '__main__':
   main()