from .localized_time import localized_now
from datetime import datetime
import json
from pathlib import Path


##reglament = [{"starts": [8, 30], "ends": [10, 5]},
##             {"starts": [10, 15], "ends": [11, 50]},
##             {"starts": [12, 20], "ends": [13, 55]},
##             {"starts": [14, 5], "ends": [15, 40]},
##             {"starts": [15, 50], "ends": [17, 25]}]

reglament = json.load(open(Path(__file__).parent/"reglament.json", "r"))

def check_pair_index():

    now = localized_now()
    now_hours, now_minutes = now.hour, now.minute # for test purpose modify here

    for pair_index, pair_start_end in enumerate(reglament, start = 1):
        start_hour = pair_start_end["starts"][0]
        start_minute =  pair_start_end["starts"][1] - 10 # so that the function can be also used at break
        if start_minute < 0:
            start_hour -= 1
            start_minute = 60 + start_minute

        end_hour = pair_start_end["ends"][0]
        end_minute =  pair_start_end["ends"][1]

        enddate = datetime(1, 1, 1, end_hour, end_minute)
        startdate = datetime(1, 1, 1, start_hour, start_minute)
        nowdate = datetime(1, 1, 1, now_hours, now_minutes)

        if check_if_in_timespan(startdate, enddate, nowdate):
            return pair_index

    return False


def check_if_in_timespan(spanstart, spanend, time):
    if (time - spanstart).total_seconds() >= 0 and (time - spanend).total_seconds() < 0:
        return True
    return False

