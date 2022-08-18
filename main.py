import os
import re
import json
import random
from dotenv import load_dotenv
from pyquery import PyQuery
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

load_dotenv() # Load your local environment variables

CHANNEL_TOKEN = os.environ.get('LINE_TOKEN')
CHANNEL_SECRET = os.getenv('LINE_SECRET')

app = FastAPI()

My_LineBotAPI = LineBotApi(CHANNEL_TOKEN) # Connect Your API to Line Developer API by Token
handler = WebhookHandler(CHANNEL_SECRET) # Event handler connect to Line Bot by Secret key

'''
For first testing, you can comment the code below after you check your linebot can send you the message below
'''
CHANNEL_ID = os.getenv('LINE_UID') # For any message pushing to or pulling from Line Bot using this ID
# My_LineBotAPI.push_message(CHANNEL_ID, TextSendMessage(text='Welcome to my pokedex !')) # Push a testing message

'''
See more about Line Emojis, references below
> Line Bot Free Emojis, https://developers.line.biz/en/docs/messaging-api/emoji-list/
'''
# Create my emoji list
my_emoji = [
    [{'index':27, 'productId':'5ac1bfd5040ab15980c9b435', 'emojiId':'005'}],
    [{'index':27, 'productId':'5ac1bfd5040ab15980c9b435', 'emojiId':'019'}],
    [{'index':27, 'productId':'5ac1bfd5040ab15980c9b435', 'emojiId':'096'}]
]

# Line Developer Webhook Entry Point
@app.post('/')
async def callback(request: Request):
    body = await request.body() # Get request
    signature = request.headers.get('X-Line-Signature', '') # Get message signature from Line Server
    try:
        handler.handle(body.decode('utf-8'), signature) # Handler handle any message from LineBot and 
    except InvalidSignatureError:
        raise HTTPException(404, detail='LineBot Handle Body Error !')
    return 'OK'

# All message events are handling at here !
@handler.add(MessageEvent, message=TextMessage)
def handle_textmessage(event):
    recieve_message = str(event.message.text)
    if recieve_message  == "#help":
        command_describtion = '$ Commands:\n\
        #<a>+<b>=\n\t->Add two numbers !\n\
        #<a>-<b>=\n\t->Subtract two numbers !\n\
        #<a>*<b>=\n\t->Multiply two numbers !\n\
        #<a>*<b>=\n\t->Divide two numbers !\n'
        My_LineBotAPI.reply_message(
            event.reply_token,
            TextSendMessage(
                text=command_describtion,
                emojis=[
                    {
                        'index':0,
                        'productId':'5ac21a18040ab15980c9b43e',
                        'emojiId':'110'
                    }
                ]
            )
        )

    elif re.findall('[a-zA-Z~`!@#$%^&_-|{}\?<>]',recieve_message):
        My_LineBotAPI.reply_message(
            event.reply_token,
            TextSendMessage(
                text = "input error ! Enter #help for commands !"
    ))
    elif "0" not in recieve_message and "1" not in recieve_message and "2" not in recieve_message and "3" not in recieve_message and "4" not in recieve_message and "5" not in recieve_message and "6" not in recieve_message and "7" not in recieve_message and "8" not in recieve_message and "9" not in recieve_message:
        My_LineBotAPI.reply_message(
            event.reply_token,
            TextSendMessage(
                text = "input error ! Enter #help for commands !"))
    else:
        try:
            ans = eval(recieve_message)
        except ZeroDivisionError:
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(
                    text = "Error : Division of zero !"))
        except SyntaxError:
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(
                    text = "input error ! Enter #help for commands !"))
        else:
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(
                    text = eval(recieve_message))
            )


# Line Sticker Class
class My_Sticker:
    def __init__(self, p_id: str, s_id: str):
        self.type = 'sticker'
        self.packageID = p_id
        self.stickerID = s_id

'''
See more about Line Sticker, references below
> Line Developer Message API, https://developers.line.biz/en/reference/messaging-api/#sticker-message
> Line Bot Free Stickers, https://developers.line.biz/en/docs/messaging-api/sticker-list/
'''
# Add stickers into my_sticker list
my_sticker = [My_Sticker(p_id='446', s_id='1995'), My_Sticker(p_id='446', s_id='2012'),
     My_Sticker(p_id='446', s_id='2024'), My_Sticker(p_id='446', s_id='2027'),
     My_Sticker(p_id='789', s_id='10857'), My_Sticker(p_id='789', s_id='10877'),
     My_Sticker(p_id='789', s_id='10881'), My_Sticker(p_id='789', s_id='10885'),
     ]

# Line Sticker Event
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    # Random choice a sticker from my_sticker list
    ran_sticker = random.choice(my_sticker)
    # Reply Sticker Message
    My_LineBotAPI.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id= ran_sticker.packageID,
            sticker_id= ran_sticker.stickerID
        )
    )
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', reload=True, host='0.0.0.0', port=8787)
                                       