import time

weekdays = [4, 5, 6]

def check_if_weekend():
    now = time.localtime()

    if now.tm_wday in weekdays:
        print("Weekday!")
        return True
    return False
