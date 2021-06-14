#import time

message_counter = {"index": 0, "timestamp_of_first_msg": 0, "timestamp_of_last_msg": 0, "session_content": []}

def register_message(message, telegram_timestamp):
    print("Some message")

    if reset_session(telegram_timestamp):
        message_counter["index"] = 0

    message_counter["index"] += 1
    message_counter["session_content"].append(message)

    if message_counter["index"] == 1:
        message_counter["timestamp_of_first_msg"] = telegram_timestamp #time.time()

    elif message_counter["index"] == 6:
        message_counter["timestamp_of_last_msg"] = telegram_timestamp
        message_counter["index"] = 0
        if check_on_flood():
            return True

        message_counter["session_content"] = []

    return False


def check_on_flood():
    then = message_counter["timestamp_of_first_msg"]
    now = message_counter["timestamp_of_last_msg"]
    overhead = 0
    if check_if_all_elements_equall(message_counter["session_content"]):
        overhead = 10

    print("timespan between first and sixth msg:", now - then)
    if now - then <= 4 + overhead:
        return True
    return False

def antiflood_reaction():
    print("It's time to stop")

def check_if_all_elements_equall(list_):
	return list_.count(list_[0]) == len(list_)

def reset_session(timestamp):
    if timestamp - message_counter["timestamp_of_first_msg"] > 14:
        return True
    return False
