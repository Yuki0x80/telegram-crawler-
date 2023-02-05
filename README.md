# telegram-crawler
## How To Use

### Configuration settings
- [TELEGRAM]
    - Accesses(https://core.telegram.org/) and make Token
- [PROXY]
    - If you want to do the proxy, You can do it.
- [EXCEPT CHANNEL]
    - For example, except for the Default channel

### Dockerfile with Docker
```
$ docker image build -t telegram-crawler:v1 .

$ docker run --name  telegram-crawler -it telegram-crawler:v1
> Please enter your phone (or bot token): <phone number>
```

### Python in local 
```
$ python -V
Python 3.10.3

$ pip install --no-cache-dir -r requirements.txt

$ python telegram_crawler.py
> Please enter your phone (or bot token): <phone number>
```

## Output Example
```
> python telegram_crawler.py
('{\n'
 '  "1xxxxxxxxx": {\n'
 '    "channel_name": "xxxxx",\n'
 '    "message_id": 11111,\n'
 '    "message": "XXXXX",\n'
 '    "message_from_geo": null,\n'
 '    "JST_send_time": "2023/06/02, 04:00:05",\n'
 '    "display_of_post_author": null,\n'
 '    "from_id": {\n'
 '      "peerUser": 1xxxxxxx\n'
 '    },\n'
 '    "sender_user": {\n'
 '      "user_id": 1xxxxxxx,\n'
 '      "username": "xxxx",\n'
 '      "phone": null,\n'
 '      "Firstname": "xxx",\n'
 '      "Lastname": null\n'
 '    },\n'
 '    "bot": false\n'
 '  }\n'
 '}')
 ...
```

## License
The source code is licensed MIT. The website content is licensed CC BY 4.0,see LICENSE.