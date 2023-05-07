from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser
import time
import os
import re
from packs import *
import asyncio
from datetime import datetime

api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
phone_number = os.environ['PHONE']
ltime=''
cronflag = False

def get_code():
    total=60
    while total > 0:
        with open('code.txt','r') as f:
            tmp = f.read()
        if bool(re.fullmatch(r'\d{5}', tmp)):
            return tmp
        print('Please place code in "code.txt".')
        time.sleep(2)
        total -=2
    return '-1'

def replace_last_line(file_name, diff):
    lines = []
    with open(file_name, 'r') as file:
        lines = file.readlines()

    addtext=f'{str(datetime.now())} Checking update interval: {diff} \n'
    
    # 检查最后一行的内容
    if 'Checking update interval' in lines[-1]:
        lines[-1] = addtext
        # 将结果写回文件
        with open(file_name, 'w') as file:
            file.writelines(lines)
    else:
        with open(file_name, 'a') as file:
            file.write(addtext)

    

#login appbot
print('Client connecting...')
client = TelegramClient('anon', api_id, api_hash)
# client.start()
client.connect()
time.sleep(3)
if not client.is_user_authorized():
    try:
        ph=client.send_code_request(phone_number)
        hash1=ph.phone_code_hash
        code1=get_code()
        if code1 != '-1':
            client.sign_in(phone_number,code1,phone_code_hash=hash1)
        else:
            print('Time out of getting code!')
            exit()
    except BaseException as e:  
        print(f'Login failed: {e}')
        exit()

if client.is_user_authorized():
    with open('code.txt','w') as f:
        f.write('')
    print('Login success.')
else:
    print(f'Login failed: {e}')
    exit()

me = client.get_me()
bll_bot = client.get_entity('freenodeshare_bot')
jt_bot = client.get_entity('jttest1st_bot')
  
# 定义事件处理器来处理新消息
@client.on(events.NewMessage(chats=[bll_bot]))
async def handle_new_message(event):
    # 检查消息是否来自目标用户
    global ltime
    if event.is_private and isinstance(event.peer_id, PeerUser) and event.peer_id.user_id == bll_bot.id:
        # 打印目标用户的回复消息
        res = event.text
        if "://" in res:
            # print(res[0:12])
            try:
                nodes, counts = text_processor(res)
                print(f"Writing {counts} nodes into file...")
                filename='data/nodes.txt'
                with open(filename, 'w') as f:
                    f.write(nodes)
                print('Nodes file saved')
            except BaseException as e:
                # 向目标用户发送消息
                await client.send_message(entity=me, message=f'Error: {e}')

    
@client.on(events.NewMessage(chats=[jt_bot]))
async def handle_new_message1(event):
    print('get update cmd...')
    res = event.text
    print(f'text: {res}')
    print(f'sender: {event.sender_id}')
    j= event.sender_id == jt_bot.id
    print(f'same as bot: {j}')
    r = res == 'update nodes'
    print(f'same as text: {r}')
    if res == 'update nodes':
        try:
            print('sending /get to bll')
            await client.send_message(entity=bll_bot, message='/get')
        except BaseException as e:
            # 向目标用户发送消息
            await client.send_message(entity=me, message=f'Error: {e}')

@client.on(events.NewMessage(chats=[bll_bot]))
async def timeupdate_command(event):
    global ltime
    match = re.search(r'\d{2}:\d{2}:\d{2}',event.text)
    if event.peer_id.user_id == bll_bot.id:
        if match:
            time_str = match.group(0)
            
            tmp = datetime.strptime(time_str, '%H:%M:%S').time()
            ltime = datetime.combine(datetime.today(), tmp)
            # ltime = newtmp.timestamp()
            # ltime=newtmp
            newtmp_str=str(ltime)
            with open('data/logs.txt','a') as f:
                f.write(f'{newtmp_str} Nodes Updated.\n')


@client.on(events.NewMessage(pattern='/loopon'))
async def start_command(event):
    global cronflag,ltime
    if event.peer_id.user_id == me.id:
        cronflag = True
        await client.send_message(entity=bll_bot, message='/get')
        testtmp=datetime.now()
        while type(ltime) != type(testtmp):
            await asyncio.sleep(5)
        
        with open('data/logs.txt','a') as f:
            f.write(f'{testtmp}: Update loop ON\n')
        await client.send_message(entity=me, message='From ClientBot: Auto-Update on!')
        
        while cronflag:
            now = datetime.now()
            diff = (now -ltime).total_seconds()
            replace_last_line('data/logs.txt',diff)
            if diff > 1800:
                await client.send_message(entity=bll_bot, message='/get')
            await asyncio.sleep(60)  # 每60秒检查一次时间差
        
        with open('data/logs.txt','a') as f:
            f.write(f'{testtmp}: Update loop OFF\n')
        await client.send_message(entity=me, message='From ClientBot: Auto-Update OFF!')


@client.on(events.NewMessage(pattern='/loopoff'))
async def stop_command(event):
    global cronflag
    if event.peer_id.user_id == me.id:
        cronflag = False



client.run_until_disconnected()

