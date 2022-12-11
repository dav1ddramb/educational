# from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import telebot
import time
import requests
import numpy as np
import re
from telebot import types
from bs4 import BeautifulSoup


bot = telebot.TeleBot(token='') ### INSERT TOKEN HERE ###

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('/get_meme')
markup.add(itembtn1)

def get_url():
    req = requests.Session()
    contents = req.get('https://random.dog/woof.json').json()
    image_url = contents['url']
    return image_url


@bot.message_handler(commands=['start'])
def start(message):
    #bot.reply_to(message, 'This bot sends random dog pics :) \nType / to see the commands available',
    #            reply_markup=markup)
    bot.reply_to(message, 'Type / to see the commands available or simply hit the button :)',
                 reply_markup=markup)

def listener(messages):
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'text':
            text = m.text
            #bot.send_message(chatid, text)
            return text


@bot.message_handler(commands=['bop'])
def bop(message):
    url = get_url()
    chat_id = message.chat.id
    #chat_id = update.message.chat_id
    bot.send_photo(chat_id, url)


dl = dict()
@bot.message_handler(commands=['add'])
def add_deadline(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'What is the event?')

    @bot.message_handler(func=lambda msg: msg.text is not None)
    def event_capture(message):
        event = message.text
        dl[event] = 'NEW'

    #bot.send_message(chat_id, 'What is the date?')
    #@bot.message_handler(func=lambda msg: msg.text is not None)
    #def date_capture(message):
     #   date = message.text
      #  global event
       # dl[event] = date

    print(dl)


@bot.message_handler(commands=['vossi_bop'])
def vossi_bop(message):
    #req = requests.Session()
    stormz_url = 'https://resources.mynewsdesk.com/image/upload/c_limit,dpr_2.625,f_auto,h_700,q_auto,w_360/m4zlv5mteblv9w9keqj5.jpg'
    #stormz_photo = req.get(stormz_url).json()
    chat_id = message.chat.id
    bot.send_photo(chat_id=chat_id, photo=stormz_url)


#@bot.message_handler(commands=['hangman'])
def hangman1(message):
    dictt = ['привет', 'день', 'свет', 'темнота', 'плотность', 'неделя']
    word_text = dictt[np.random.randint(0, len(dictt))].upper()
    word_letters = set([word_text[y].upper() for y in range(len(word_text))])
    hid = ['_'] * len(word_text)
    guessed = set()
    n_mist = 0
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text=' '.join(hid))
    while n_mist < 7:
        let = message.text
        if len(let) > 1:
            bot.send_message(chat_id=chat_id, text='Enter one letter :)')
            bot.send_message(chat_id=chat_id, text=' '.join(hid))
        else:
            if let in word_letters:
                if let in guessed:
                    bot.send_message(chat_id=chat_id, text='You have alredy guessed {}'.format(let))
                    bot.send_message(chat_id=chat_id, text=' '.join(hid))
                    bot.send_message(chat_id=chat_id, text='You have alredy guessed {}'.format(let))
                    bot.send_message(chat_id=chat_id, text=' '.join(hid))
                else:
                    guessed.update(let)
                    if guessed & word_letters == word_letters:
                        bot.send_message(chat_id=chat_id, text='С победой!')
                        bot.send_message(chat_id=chat_id, text='The word is {}'.format(word_text))
                        break
                    else:
                        ind = [m.start() for m in re.finditer(let, word_text)]
                        for i in ind:
                            hid[i] = let.upper()
                        bot.send_message(chat_id=chat_id, text=' '.join(hid))
            else:
                n_mist += 1
                guessed.update(let)
                bot.send_message(chat_id=chat_id, text='Wrong letter! Mistakes: {}'.format(n_mist))
                bot.send_message(chat_id=chat_id, text=' '.join(hid))
        if n_mist == 7:
            bot.send_message(chat_id=chat_id, text='You have lost. The word is {}'.format(word_text))



@bot.message_handler(commands=['get_meme'])
def get_meme(message):
    url = 'https://www.reddit.com/r/meme/'
    headers = {'user-agent': 'Mozilla/5.0 '}
    res = requests.get(url, headers=headers)
    cont = res.content
    tree = BeautifulSoup(cont, 'html.parser')
    #print(len(tree.find_all('img', {'alt': 'Post image'})))
    pic = tree.find_all('img', {'alt': 'Post image'})[np.random.randint(0, len(tree.find_all('img', {'alt': 'Post image'})))]['src']
    chat_id = message.chat.id
    bot.send_photo(chat_id, pic)


d = dict()      # upload from a file not to lose data after reset
@bot.message_handler(func=lambda msg: msg.text is not None and '-' in msg.text)
def add_dl(message):
    userid = message.from_user.id
    d[userid] =[message.text.split('-')[0], message.text.split('-')[1]]
    #d[userid]['d'] = message.text.split('-')[1]
    print(message)
    print(d)


@bot.message_handler(commands=['see'])
def see_dl(message):
    userid = message.from_user.id
    chat_id = message.chat.id
    #bot.send_message(chat_id, d[userid]['e'] + ' till ' + d[userid]['d'])
    bot.send_message(chat_id, d[userid][0] + ' ' + d[userid][1])

@bot.message_handler(commands=['fwd'])
def fwd_message(message):
    # userid = message.from_user.id
    chat_id = message.chat.id
    from_chat_id = '@worldinmapstg'
    print(message)
    # print(message.message_id)
    # print(message['message_id'])

    # test_message = bot.send_message(from_chat_id, 'Test!')
    # test_message_id = test_message.message_id

    lastmessageid =  1001 #1437 # message.message_id    # message['message_id'] # message[-1].message_id
    # username = 'daviddramb'
    for i in range(1000, 1400):
        try:
            bot.forward_message(chat_id, from_chat_id, i)
        except:
            pass
    # bot.send_message(chat_id, d[userid]['e'] + ' till ' + d[userid]['d'])
    # bot.send_message(chat_id, d[userid][0] + ' ' + d[userid][1])


@bot.message_handler(func=lambda msg: msg.text is not None)
def answer(message):
    text = message.text
    bot.reply_to(message, '{} command is not available YET'.format(text))

# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.text)

#bot.set_update_listener(listener)

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)