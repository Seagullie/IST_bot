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
        self.owner_chat_id = 689942888
        self.initiator_whitelist = [self.group_chat_id, self.owner_chat_id]
        self.special_whitelist = [self.group_chat_id, self.owner_chat_id]
        
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
            classroom_number = choice(["???", "??\_(???)_/??"])
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

    def execute_callbacks(self, content_type, telegram_timestamp, chat_id, update, message_mode):
        
        if content_type == 'text':
            print("the bot got something of type 'text'")

            text = update[message_mode]['text'].lower()
            print("to be more precise,", text)
            if chat_id in self.special_whitelist and  register_message(text, telegram_timestamp):
                self.onflood_responses[randint(0, len(self.onflood_responses) - 1)](chat_id)

            # if text.lower().startswith("?????? ??????") or text.lower().startswith("?????? ??????"):
            #     tell_classroom(chat_id)

            elif text.startswith("ist_bot echo in group chat"):
                echo = " ".join(update[message_mode]['text'].split(" ")[5::])
                self.echo_in_group_chat(self.group_chat_id, echo)

            elif text == "/help" or text == r"/help@Chaiko_bot".lower():
                if chat_id in self.special_whitelist:
                    help_message = self.help_message()
                else: 
                    help_message = self.help_message() # will handle it in a special way. Not now
                    
                self.bot.sendMessage(chat_id, help_message)

            elif text == "????????":
                responses = ["??????????", "?????? ???? ???? ???? ???? ???? ???? ???? ???? ???? ???? ?????????? ???? ???? ???? ???? ???? ???? ???? ???? ???? ???? ???????? ???? ???? ???? ?????????? ???? ???? ???? ???? ???? ???? ???? ???? ???? ???? ???? ???? ?? ???? ???? ???? ???? ???? ????  ???? ????", "????????", "????????", "????????", "??????????", "???????", "<b>????????</b>"]
                self.bot.sendMessage(chat_id, choice(responses), parse_mode = 'HTML')

            elif text == "??????":
                self.bot.sendMessage(chat_id, choice(["????????????", "????????????", "????????????", "<s>????????</s>????????????"]), parse_mode = 'HTML')

            elif text == "/kit" or text == "/kit@Chaiko_bot".lower():
                cat_pic__link = get("https://api.thecatapi.com/api/images/get?format=json" + choice(["", "&type=gif"])).json()[0]['url']
                if cat_pic__link.endswith("gif"):
                    self.bot.sendDocument(chat_id, cat_pic__link)
                else:
                    self.bot.sendPhoto(chat_id, cat_pic__link)

        elif content_type in ['document', 'photo'] and chat_id in self.special_whitelist:
            
            file_size = update[message_mode][content_type]['file_size']
            
            if content_type == 'document':
                if register_message(file_size, telegram_timestamp):
                    choice(self.onflood_responses)(chat_id)

            elif content_type == 'photo':
                if register_message(file_size, telegram_timestamp):
                    choice(self.onflood_responses)(chat_id)

            elif content_type == 'sticker':
                if register_message(update[message_mode][content_type]['set_name'], telegram_timestamp):
                    choice(self.onflood_responses)(chat_id)
    
    def get_message_mode(self, incoming_message):

        try:
            # content_type, chat_type, chat_id = telepot.glance(incoming_message['message'])
            telepot.glance(incoming_message['message'])
            message_mode = 'message'
        except KeyError:

            try:
                # content_type, chat_type, chat_id = telepot.glance(incoming_message['edited_message'])
                incoming_message['edited_message']
            except KeyError as e:
                print(e)
                return "mode not supported"

            message_mode = 'edited_message'
            
        return message_mode
    
    def initiator_in_whitelist(self, chat_id):
        # return chat_id in self.initiator_whitelist
        return True # the open mode
    
    def handle_incoming_message(self):
        update = request.get_json()
        message_mode = self.get_message_mode(update)
        
        if message_mode == "mode not supported": return "OK"
        
        content_type, chat_type, chat_id = telepot.glance(update['message'])

        telegram_timestamp = update[message_mode]['date']
        self.send_debug_info(update, content_type, chat_type, chat_id)

        if not self.initiator_in_whitelist(chat_id) or not self.check_if_recent(update[message_mode]['date']):
            return "OK"

        return self.execute_callbacks(content_type, telegram_timestamp, chat_id, update, message_mode)
        

bot = IST_bot()

@app.route(f'/{secret}', methods=["POST"])
def handle_incoming_message():
    try:
        bot.handle_incoming_message()
        return "OK"
    except Exception as e:
        print(e)
        return "OK"

