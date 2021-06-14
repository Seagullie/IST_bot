import json
from .check_pair_index import check_pair_index
from .localized_time import localized_now
from .check_if_weekend import check_if_weekend
from .check_if_week_is_even import check_if_week_is_even
import calendar
from pathlib import Path

schedule = json.load(open(Path(__file__).parent/"schedule.json", encoding="utf-8"), parse_int = int)

def get_current_pair():
    current_pair_index = str(check_pair_index())
    studytime = check_if_studytime(current_pair_index)
    if studytime != True:
        return studytime
    weekday = localized_now().weekday()
    weekday_verbal = get_weekday_name(weekday)
    try:
        specific_pair_data = schedule[weekday_verbal][current_pair_index]
    except KeyError:
        return False
    return specific_pair_data

def get_weekday_name(index):
    weekday_names = list(calendar.day_name)
    return weekday_names[index]

def check_if_studytime(current_pair_index):
    if current_pair_index == 'False':
        return "No pairs right now"
    if check_if_weekend():
        return "Weekend"
    return True

def extract_pair_parity(pair_data):
    if type(pair_data) == list:
            parity = pair_data[check_if_week_is_even() == "even"]["parity"]

    else:
        try:
            parity = pair_data["parity"]

        except KeyError:
            return False

    return parity

