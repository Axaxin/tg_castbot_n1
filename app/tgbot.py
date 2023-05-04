# Importing Required Libraries, Imported os Module For Security 
from threading import Thread
import telebot
import time
import os
from packs import *
# from flask import Flask

# Getting Bot Token From Secrets
BOT_TOKEN = os.environ.get('BOT_TOKEN')

authuser=['QuadraQ','FatEast']
adminid=0
looplock=True
cronflag=False
lasttime=0

# Creating Telebot Object
bot = telebot.TeleBot(BOT_TOKEN)


# app=Flask(__name__)

# @app.route('/')
# def homepage():
#   return '<h1>Hello World!</h1>'

# @app.route('/sub')
# def subtxt():
#   with open('nodes.txt','r') as f:
#     nodes=f.read()
#   return nodes


@bot.message_handler(commands=['start'])
def startup(message):
    chatid=message.chat.id
    user=message.from_user
    if user.username in authuser:
        bot.send_message(chatid,'Hello,WhaleCum!')

@bot.message_handler(commands=['link'])
def linkin(message):
    global adminid
    user=message.from_user
    if user.username in authuser:
        adminid = user.id
        bot.send_message(adminid,f'Admin: {user.username} id: {adminid}')


@bot.message_handler(commands=['update'])
def update_nodes(message):
    global adminid
    chatid = message.chat.id
    # full = message.text
    username=message.from_user.username
    if username in authuser:
        try:
            bot.send_message(adminid,'update nodes')
        except BaseException as e:
            print(f'Something wrong, {e}')
            bot.send_message(chatid, f"Something goes wrong: {e}")

    
@bot.message_handler(commands=['loop'])
def update_loop(message):
    global cronflag
    chatid = message.chat.id
    full = message.text
    content = full.split(' ')[-1]
    reply =''
    if content == 'on':
        cronflag=True
        reply='loop on'
    elif content == 'off':
        cronflag = False
        reply ='loop off'
    else:
        reply='Unknown command.'
    bot.send_message(chatid, reply)
    # lasttime=formattime(lastupdate)
    # bot.send_message(chatid, f"{reply} Last update at: {lasttime}")
          
@bot.message_handler(commands=['shutdown'])
def command_dc(message):
    global looplock,cronflag,bot,adminid
    user=message.from_user
    if user.username in authuser:
        print('shutting down...')
        looplock=False
        cronflag = False
        bot.stop_polling()
        exit()
    else:
      print('Not admin')
      # bot.reply_to(,'you are not admin.')

@bot.message_handler(content_types=['document'])
def command_handle_document(message):
    global lasttime
    user = message.from_user
    
    if user.username in authuser:
        # 获取文档信息
        document_info = message.document
        # 获取文件ID
        file_id = document_info.file_id
        # 获取文件名
        file_name = document_info.file_name
        # 使用文件ID下载文件
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # 将文件保存到本地
        with open(file_name, 'wb') as f:
            f.write(downloaded_file)
        
        lasttime=time.time()
        # bot.send_message(message.chat.id, 'Document received, sir!')

# @bot.message_handler(func=lambda message: True)
# def process(message):
#     pass
    
def run_bot():
    print('Bot up...')
      
    # Waiting For New Messages
    bot.polling()
  
    print('Bot down...')
    time.sleep(3)
    exit()

def run_flask():
  global app
  app.run(host='0.0.0.0',port=8080)
    
def crontask():
    global looplock,cronflag,lasttime
    while looplock:
        if cronflag and time.time()-lasttime > 1800:
            bot.send_message(adminid,'update nodes')
        time.sleep(2)
    print('loop ends')



cron_th=Thread(target=crontask)
cron_th.start()

print('Bot up...')
bot.polling()
print('Bot down...')

# app.run(host='0.0.0.0',port=8080)


