from telethon import TelegramClient, events
from telethon.tl.custom import Message
import configparser
import datetime
import socks
import json
import pprint
import traceback

class TelegramCrawler:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        api_id      = config.get('TELEGRAM', 'api_id')
        api_hash    = config.get('TELEGRAM', 'api_hash')
        proxy       = self.set_proxy(config)
        self.exception_list = config.get('EXCEPT CHANNEL', 'channel')
        self.exception_list = self.exception_list.replace(" ","").split(',')

        # start telegram client
        self.telegram_client = TelegramClient('CAnonBot', api_id, api_hash, proxy=proxy)
        self.telegram_client.start()
        self.telegram_client.add_event_handler(self.new_message_handler, events.NewMessage(incoming=True))
        self.set_own_channel_list()

    def set_proxy(self, config):
        proxy_type  = config.get('PROXY', 'type')
        proxy_addr  = config.get('PROXY', 'addr')
        proxy_port  = config.get('PROXY', 'port')
        proxy_username = config.get('PROXY', 'username')
        proxy_password = config.get('PROXY', 'password')
        
        # proxy setting & checking
        if proxy_type == "HTTP": proxy_type = socks.HTTP
        elif proxy_type == "SOCKS4": proxy_type = socks.SOCKS4
        elif proxy_type == "SOCKS5": proxy_type = socks.SOCKS5
        else: proxy_type = None

        proxy_addr = proxy_addr if proxy_addr != "" else None
        proxy_port = int(proxy_port) if proxy_port.isdigit() else None
        proxy_username = proxy_username if proxy_username != "" else None
        proxy_password = proxy_password if proxy_password != "" else None

        if proxy_type != None and proxy_addr != None and proxy_port != None \
            and proxy_username != None and proxy_password != None:
            proxy = (proxy_type, proxy_addr, proxy_port, False, proxy_username, proxy_password)
        else: proxy = None

        return proxy

    def set_own_channel_list(self):
        self.channel_list = {}
        for dialog in self.telegram_client.iter_dialogs(ignore_pinned=True):
            self.channel_list[str(dialog.id)] = {"channel_name": dialog.name}
            if dialog.entity.username != None: 
                self.channel_list[str(dialog.id)].update({"channel_url": "t.me/" + dialog.entity.username})

    # Waiting new message
    async def new_message_handler(self, event: events.NewMessage.Event):
        message_logs = {}
        message: Message    = event.message
        sender              = await event.get_sender()
        chennel_info        = await event.get_input_chat()

        chennel_id                  = chennel_info.channel_id
        message_logs[chennel_id]    = {}
        channel_name                = self.channel_list['-100' + str(chennel_id)]["channel_name"]
        
        # excpet channel
        for except_list in self.exception_list:
            if except_list in channel_name.replace(" ",""): return

        # message from user
        message_logs[chennel_id]["channel_name"]       =  channel_name
        message_logs[chennel_id]["message_id"]         =  message.id
        message_logs[chennel_id]["message"]            =  message.raw_text
        message_logs[chennel_id]["message_from_geo"]   =  message.geo
        message_logs[chennel_id]["JST_send_time"]          =  self.utc_to_jts(message.date)
        message_logs[chennel_id]["display_of_post_author"] =  message.post_author

        # four type of message
        if hasattr(message.from_id, "user_id") == True: 
            message_logs[chennel_id]["from_id"] = {"peerUser": message.from_id.user_id}

        elif hasattr(message.from_id, "chat_id") == True:
            message_logs[chennel_id]["from_id"] = {"peerChat": message.from_id.chat_id}

        elif hasattr(message.from_id, "channel_id") == True:
            message_logs[chennel_id]["from_id"] = {"peerChannel": message.from_id.channel_id}

        else: message_logs[chennel_id]["from_id"] = {"anonymous": None}

        # if it wasn't a bot, get user data
        if sender.bot != True:
            message_logs[chennel_id]["sender_user"] = {"user_id": sender.id, "username": sender.username,  \
                 "phone": sender.phone, "Firstname": sender.first_name, "Lastname": sender.last_name}
        message_logs[chennel_id]["bot"] = sender.bot

        # output:JSON
        self.json_telegram_message_data = json.dumps(message_logs, indent=2, ensure_ascii=False)
        pprint.pprint(self.json_telegram_message_data)
    
    def utc_to_jts(self, date_time):
        try:
            date_time = date_time.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
            date_time = date_time.strftime("%Y/%d/%m, %H:%M:%S")
            return date_time
        except:
            traceback.print_exc()
            return None
    
    # reset telegram client session
    def logout_from_telegram_session(self):
        self.telegram_client.log_out()

if __name__ == "__main__":
    abc = TelegramCrawler()
    abc.telegram_client.run_until_disconnected()