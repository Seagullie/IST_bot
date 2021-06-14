from .localized_time import localized_now
from datetime import datetime

#starttime = datetime (2020, 1, 1)

def check_if_week_is_even(starting_point = datetime(2020, 2, 22)):# <-- for test
    # purpose modify here
    elapsed__in_seconds = (localized_now() - starting_point).total_seconds()

    elapsed_in_weeks = elapsed__in_seconds/(60*60*24*7)

    if (int(elapsed_in_weeks) + 1) % 2 == 0:
        return "even"
    else:
        return "odd"
