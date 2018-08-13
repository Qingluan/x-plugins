import os
from qlib.data import dbobj, Cache
try:
    from telethon import TelegramClient, sync
    from telethon.errors import SessionPasswordNeededError
    from telethon.tl.types import  MessageMediaDocument
    from telethon.utils import get_display_name
except Exception as e:
    os.popen("pip3 install telethon && sleep 1").read()
    from telethon import TelegramClient, sync
    from telethon.errors import SessionPasswordNeededError
    from telethon.tl.types import  MessageMediaDocument
    from telethon.utils import get_display_name

if not os.path.exists(os.path.expanduser("~/.ssh/id_rsa.pub")):
    os.popen("mkdir -p ~/.ssh/ && ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa")
import logging
logging.basicConfig(level=logging.INFO)

DB_PATH = os.path.expanduser("~/.db.sql")


client = None
tloop = None

class Token(dbobj):
    pass


def connect(phone, token,loop=None):
    global client
    api_id, api_hash = token.split(":")
    api_id = int(api_id)
    
    client = TelegramClient('session', api_id=api_id, api_hash=api_hash, loop=loop)
    client.connect()
    return client


def set_token(token):
    c = Cache(DB_PATH)
    if not c.query_one(Token):
        t = Token(tp='tel', token=token)
        t.save(c)
    else:

        if client and client.is_user_authorized():
            t = Token(tp='tel', token=token)
            t.save(c)   


def send_code(phone):
    client.send_code_request(phone)

def login(phone, code):
    # Ensure you're authorized
    if not client.is_user_authorized():
        try:
            client.sign_in(phone, code)
        except SessionPasswordNeededError:
            return 'auth fail .. need password ??'
    me = client.get_me()
    if me:
        return "auth ok"
    return 'auth fail'


def run(cmd, phone=None, token=None, code=None, loop=None):
    """
    args=set token=xxx:xxxxxx # set token init
    args=set token=xxx:xxxxxx phone=xxxxxx code=xxxx # set token by auth telegram
    args=auth token=xxx:xxxxxx phone=xxxxxx # will lei server send code to your tele
    args=login token=xxx:xxxxx phone=xxxxx code=xxxxxx  #login
    


    """
    global tloop
    
    if not loop:
        logging.info("no loop")
    else:
        logging.info("loop")

    tloop = loop
    if cmd == 'set':
        if phone and token and code:
            connect(phone, token, loop)
            send_code(phone)
            login(phone, code)

        set_token(token)
        
        return 'set token ok'
    elif cmd == 'auth':
        c = Cache(DB_PATH)
        if not c.query_one(Token, token=token.strip()):
            return "not token : %s found in db." % token
        connect(phone, token, loop)
        send_code(phone)
        if code:
            login(phone, code)
        return 'send code to your telegram device.'
    elif cmd == 'login':
        c = Cache(DB_PATH)
        if not c.query_one(token=token.strip()):
            return "not token : %s found in db." % token
        connect(phone, token,loop)
        return login(phone, code)




