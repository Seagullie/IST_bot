from flask import Flask, request
import telepot
import urllib3
from pprint import pformat
from antiflood_reaction import register_message
from random import randint, choice
from tell_room_number__academy import report_pair_data
from time import time
from requests import get

#proxy stuff
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
#proxy stuff

secret = 123123
bot = telepot.Bot('1059909995:AAHj400Laz83QuY5pmIEnmE_rseaEup2Ct4')
bot.setWebhook(f"https://seagullie.pythonanywhere.com/{secret}", max_connections=1)
onflood_responses = [
lambda chat_id: bot.sendVideo(chat_id, open("ahahaha_u_great.mp4", "rb"))]#lambda chat_id: bot.sendPhoto(chat_id, open("munch_munch_aAaaAAA", "rb")),
group_chat_id = -1001230414615

def help_message():
    with open("help_text.txt", "r", encoding = "utf-8") as help_text:
        bot_description = help_text.read()

    return bot_description

def check_if_recent(message_timestamp):
    now = time()

    if now - message_timestamp > 1 * 30:
        return False

    return True

app = Flask(__name__)

def echo_back(update, chat_id):
    if "text" in update["message"]:
        text = update["message"]["text"]
        bot.sendMessage(chat_id, f"From the web: you said '{text}'")
    else:
        bot.sendMessage(chat_id, "From the web: sorry, I didn't understand that kind of message")

def tell_classroom(chat_id):
    classroom_number = str(report_pair_data.report_pair_room())
    if not classroom_number.isnumeric():
        classroom_number = choice(["✕", "¯\_(ツ)_/¯"])
    bot.sendMessage(chat_id, classroom_number)

def log_message(message):

    with open("message2.log", "a") as log:
        log.write(message)

def send_debug_info(update, content_type, chat_type, chat_id):
    debug_info = "Debug info:\n" + pformat(update)
    debug_info__summary = f"Debug info. A glance:\nContent type: {content_type}\nChat type: {chat_type}\nChat id:{chat_id}"
    log_message("\n" + debug_info + "\n\n" + debug_info__summary + "\n--------")
    if chat_id != 689942888:
        return

    bot.sendMessage(chat_id, debug_info)
    bot.sendMessage(chat_id, debug_info__summary)

def echo_in_group_chat(group_chat_id, message):
    bot.sendMessage(group_chat_id, message)

@app.route(f'/{secret}', methods=["POST"])
def telegram_webhook():
    update = request.get_json()

    try:
        content_type, chat_type, chat_id = telepot.glance(update['message'])
        message_mode = 'message'
    except KeyError:

        try:
            content_type, chat_type, chat_id = telepot.glance(update['edited_message'])
        except KeyError as e:
            print(e)
            return "OK"

        message_mode = 'edited_message'

    telegram_timestamp = update[message_mode]['date']
    send_debug_info(update, content_type, chat_type, chat_id)

    #echo_back(update, chat_id)

    if chat_id not in(689942888, -1001230414615) or not check_if_recent(update[message_mode]['date']):
        return "OK"

    if content_type == 'text':
        print("the bot got something of type 'text'")

        text = update[message_mode]['text'].lower()
        print("to be more precise,", text)
        if register_message(text, telegram_timestamp):
            #bot.sendMessage(chat_id, "It's time to stop")
            onflood_responses[randint(0, len(onflood_responses) - 1)](chat_id)


        # if text.lower().startswith("яка ауд") or text.lower().startswith("яка авд"):
        #     tell_classroom(chat_id)

        # elif "розклад" == text:
        #     bot.sendPhoto(chat_id, "AgACAgIAAxkBAAIVGF5dFKgcfxg6kFgixoaZ75uGVKY4AAI_rTEb3WvpSqICkmkcWlSp613LDgAEAQADAgADeQADw9sCAAEYBA")
        #     #bot.sendMessage(chat_id, "sent you the schedule. enjoy :3 :3")

        elif text.startswith("ist_bot echo in group chat"):
            echo = " ".join(update[message_mode]['text'].split(" ")[5::])
            echo_in_group_chat(group_chat_id, echo)

        elif text == "/help" or text == r"/help@Chaiko_bot".lower():
            bot.sendMessage(chat_id, help_message())

        elif text == "жопа":
            responses = ["Ж😯па", "Ж̴̂ ̽͝ ̛̑ ͆͒ ̀͠ ̃̚ ̈́̈́ ̀̂ ̆̄ ̎̇ ̋́ ̢̫о̸̀ ͍͖ ̡̺ ̖͜ ͔̣ ͔̘ ̖̼ ̭̱ ̦̤ ̬̗ ̟̝ ̥͔п̷ ͆͂ ̉̋ ̘̯ ͎̮а̵̓ ͑͂ ̛̃ ̾̏ ̔̾ ́̀ ́͝ ́͗ ̀́ ̈́̒ ̀́ ̈̅ ͗̇ ̓ ̥͙ ̨̺ ̱͖ ̗̝ ͕̞ ͔̲  ͎̝ ̢̠", "жОПа", "ЖОПА", "жОПА", "Ж😮па", "Міш?", "<b>Жопа</b>"]
            bot.sendMessage(chat_id, choice(responses), parse_mode = 'HTML')
            #bot.sendPhoto(chat_id, "AgACAgIAAxkBAAIemF5fvwT7BZdU7thAvzvFSFxT8GyGAAJOrDEb4CoAAUu6HRvFo65Ka7nEwg8ABAEAAwIAA3kAAy1bBAABGAQ")

        elif text == "іст":
            bot.sendMessage(chat_id, choice(["Лідери", "Лідери", "Лідери", "<s>Жопа</s>Лідери"]), parse_mode = 'HTML')

            #

        elif text == "/kit" or text == "/kit@Chaiko_bot".lower():
            cat_pic__link = get("https://api.thecatapi.com/api/images/get?format=json" + choice(["", "&type=gif"])).json()[0]['url']
            if cat_pic__link.endswith("gif"):
                bot.sendDocument(chat_id, cat_pic__link)
            else:
                bot.sendPhoto(chat_id, cat_pic__link)




    elif content_type == 'document':
        if register_message(update[message_mode][content_type]['file_size'], telegram_timestamp):
            onflood_responses[randint(0, len(onflood_responses) - 1)](chat_id)

    elif content_type == 'photo':
        if register_message(update[message_mode][content_type][0]['file_size'], telegram_timestamp):
            onflood_responses[randint(0, len(onflood_responses) - 1)](chat_id)

    elif content_type == 'sticker':
        if register_message(update[message_mode][content_type]['set_name'], telegram_timestamp):
            onflood_responses[randint(0, len(onflood_responses) - 1)](chat_id)

    return "OK"


