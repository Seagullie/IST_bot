from flask import Flask, request
import telepot
import urllib3
from pprint import pformat
from antiflood_reaction import register_message
from random import randint, choice
from tell_room_number__academy import report_pair_data
from time import time
from requests import get

import json 

# #proxy stuff
# proxy_url = "http://proxy.server:3128"
# telepot.api._pools = {
#     'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
# }
# telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# #proxy stuff

credentials = json.load(open("credentials.json"))
secret = credentials["secret"]

app = Flask(__name__)

class IST_bot: 
    
    def __init__(self):
        self.set_proxy()
        self.set_webhook()
        self.group_chat_id = -1001230414615
        
        self.onflood_responses = [
            lambda chat_id: self.bot.sendVideo(chat_id, open("ahahaha_u_great.mp4", "rb"))]
    
    def set_proxy(self):
        #proxy stuff
        proxy_url = "http://proxy.server:3128"
        telepot.api._pools = {
            'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
        }
        telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
        #proxy stuff
        
    def set_webhook(self):
        credentials = json.load(open("credentials.json"))

        secret = credentials["secret"]
        key = credentials["key"]
        self.bot = bot = telepot.Bot(f'{key}')
        webhook = f"https://seagullie.pythonanywhere.com/{secret}"
        bot.setWebhook(webhook, max_connections=1)

    def help_message(self):
        with open("help_text.txt", "r", encoding = "utf-8") as help_text:
            bot_description = help_text.read()

        return bot_description

    def check_if_recent(self, message_timestamp):
        now = time()

        if now - message_timestamp > 1 * 30:
            return False

        return True

    def echo_back(self, update, chat_id):
        if "text" in update["message"]:
            text = update["message"]["text"]
            self.bot.sendMessage(chat_id, f"From the web: you said '{text}'")
        else:
            self.bot.sendMessage(chat_id, "From the web: sorry, I didn't understand that kind of message")

    def tell_classroom(self, chat_id):
        classroom_number = str(report_pair_data.report_pair_room())
        if not classroom_number.isnumeric():
            classroom_number = choice(["✕", "¯\_(ツ)_/¯"])
        self.bot.sendMessage(chat_id, classroom_number)

    def log_message(self, message):

        with open("message2.log", "a") as log:
            log.write(message)

    def send_debug_info(self, update, content_type, chat_type, chat_id):
        debug_info = "Debug info:\n" + pformat(update)
        debug_info__summary = f"Debug info. A glance:\nContent type: {content_type}\nChat type: {chat_type}\nChat id:{chat_id}"
        self.log_message("\n" + debug_info + "\n\n" + debug_info__summary + "\n--------")
        if chat_id != 689942888:
            return

        self.bot.sendMessage(chat_id, debug_info)
        self.bot.sendMessage(chat_id, debug_info__summary)

    def echo_in_group_chat(self, group_chat_id, message):
        self.bot.sendMessage(group_chat_id, message)

    
    def handle_incoming_message(self):
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
        self.send_debug_info(update, content_type, chat_type, chat_id)

        #echo_back(update, chat_id)

        if chat_id not in(689942888, -1001230414615) or not self.check_if_recent(update[message_mode]['date']):
            return "OK"

        if content_type == 'text':
            print("the bot got something of type 'text'")

            text = update[message_mode]['text'].lower()
            print("to be more precise,", text)
            if register_message(text, telegram_timestamp):
                #bot.sendMessage(chat_id, "It's time to stop")
                self.onflood_responses[randint(0, len(self.onflood_responses) - 1)](chat_id)


            # if text.lower().startswith("яка ауд") or text.lower().startswith("яка авд"):
            #     tell_classroom(chat_id)

            elif text.startswith("ist_bot echo in group chat"):
                echo = " ".join(update[message_mode]['text'].split(" ")[5::])
                self.echo_in_group_chat(self.group_chat_id, echo)

            elif text == "/help" or text == r"/help@Chaiko_bot".lower():
                self.bot.sendMessage(chat_id, self.help_message())

            elif text == "жопа":
                responses = ["Ж😯па", "Ж̴̂ ̽͝ ̛̑ ͆͒ ̀͠ ̃̚ ̈́̈́ ̀̂ ̆̄ ̎̇ ̋́ ̢̫о̸̀ ͍͖ ̡̺ ̖͜ ͔̣ ͔̘ ̖̼ ̭̱ ̦̤ ̬̗ ̟̝ ̥͔п̷ ͆͂ ̉̋ ̘̯ ͎̮а̵̓ ͑͂ ̛̃ ̾̏ ̔̾ ́̀ ́͝ ́͗ ̀́ ̈́̒ ̀́ ̈̅ ͗̇ ̓ ̥͙ ̨̺ ̱͖ ̗̝ ͕̞ ͔̲  ͎̝ ̢̠", "жОПа", "ЖОПА", "жОПА", "Ж😮па", "Міш?", "<b>Жопа</b>"]
                self.bot.sendMessage(chat_id, choice(responses), parse_mode = 'HTML')

            elif text == "іст":
                self.bot.sendMessage(chat_id, choice(["Лідери", "Лідери", "Лідери", "<s>Жопа</s>Лідери"]), parse_mode = 'HTML')

            elif text == "/kit" or text == "/kit@Chaiko_bot".lower():
                cat_pic__link = get("https://api.thecatapi.com/api/images/get?format=json" + choice(["", "&type=gif"])).json()[0]['url']
                if cat_pic__link.endswith("gif"):
                    self.bot.sendDocument(chat_id, cat_pic__link)
                else:
                    self.bot.sendPhoto(chat_id, cat_pic__link)

        elif content_type == 'document':
            if register_message(update[message_mode][content_type]['file_size'], telegram_timestamp):
                self.onflood_responses[randint(0, len(self.onflood_responses) - 1)](chat_id)

        elif content_type == 'photo':
            if register_message(update[message_mode][content_type][0]['file_size'], telegram_timestamp):
                self.onflood_responses[randint(0, len(self.onflood_responses) - 1)](chat_id)

        elif content_type == 'sticker':
            if register_message(update[message_mode][content_type]['set_name'], telegram_timestamp):
                self.onflood_responses[randint(0, len(self.onflood_responses) - 1)](chat_id)

        return "OK"

bot = IST_bot()

@app.route(f'/{secret}', methods=["POST"])
def handle_incoming_message():
    bot.handle_incoming_message()

