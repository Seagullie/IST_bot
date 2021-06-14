from pytz import timezone 
from datetime import datetime
import time 

def localized_now(timezone_name = 'Europe/Kiev', return_naive = True):
    gmt_now = time.gmtime()
    utc = timezone('UTC')
    utc_now = datetime(*gmt_now[:6], tzinfo=utc)
    western_timezone = timezone(timezone_name)
    western_now = western_timezone.normalize(utc_now)
    if return_naive:
        return datetime(*western_now.timetuple()[:6])
    return western_now

    # it doesn't include weekday
    # D:
    # actually, datetime object has a method named 'weekday' 

if __name__ == "__main__":
    print(localized_now())
