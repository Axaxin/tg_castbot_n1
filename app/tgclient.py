from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerUser
import time
import os
import re
from packs import *

api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
phone_number = os.environ['PHONE']

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

print('Login success.')
me = client.get_me()
bll_bot = client.get_entity('freenodeshare_bot')
jt_bot = client.get_entity('jttest1st_bot')
  
# 定义事件处理器来处理新消息
@client.on(events.NewMessage(chats=[bll_bot]))
async def handle_new_message(event):
    # 检查消息是否来自目标用户
    global lastupdate
    if event.is_private and isinstance(event.peer_id, PeerUser) and event.peer_id.user_id == bll_bot.id:
        # 打印目标用户的回复消息
        res = event.text
        if "://" in res:
            # print(res[0:12])
            try:
                nodes, counts = text_processor(res)
                print(f"Writing {counts} nodes into file...")
                filename='nodes.txt'
                with open(filename, 'w') as f:
                  f.write(nodes)
                lastupdate=time.time()
                # ftime=formattime(lastupdate)
                await client.send_file(entity=jt_bot,file=filename)
                print('File Sent.')
            except BaseException as e:
                # 向目标用户发送消息
                await client.send_message(entity=me, message=f'Error: {e}')
    print("Listening to freenodeshare_bot...")
    
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
    

client.run_until_disconnected()

