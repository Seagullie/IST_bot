from telegram.ext import Updater, CommandHandler, MessageHandler, Filters 
import requests
import re
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id 
    bot.send_photo(chat_id=chat_id, photo=url)

def echo(bot, update):
    print("got in echo function")
    chat_id__extracted = update.message.chat_id # this part is okay. Don't edit it 
    print("chat id is:", chat_id__extracted)
    message = update.message['text']
    print("message is:", message)
    bot.send_message(chat_id = chat_id__extracted, text = message)

def schedule(bot, update):
    print("sending schedule")
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open(r'Розклад пар_3_ver_4.jpg', "br"))
    #help(bot.send_photo)

##def echo(update, context):
##    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def exit__bot(bot, update):
    chat_id__extracted = update.message.chat_id
    message = "Exiting..."
    bot.send_message(chat_id = chat_id__extracted, text = message)
    exit()

def main():
    updater = Updater('1059909995:AAGU0bU7uBkYDsYFyfT1fxEMlyHI4c8Zne4')
    dp = updater.dispatcher 
    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(CommandHandler('schedule', schedule))
    dp.add_handler(CommandHandler('exit', exit__bot))
    updater.start_polling() 
    updater.idle() 

if __name__ == '__main__':
    main()
