import random
import requests
import re
import bs4
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)


line_bot_api = LineBotApi('r3LkADsx0LBEyvbPMlOUjrwaoeI4zU1LqUcm55ekeXIfS8kRJEY2FgkFST5zRodK55R9YMh/Bt6heFJkPXuyxagimhdLnyXU+o00VWYywdCxkBm1FXUFnrmyPcDVJIYJ5/aUS7FbaqvJUKFAWl0IowdB04t89/1O/w1cDnyilFU=')
                          
handler = WebhookHandler('1df2b26ef5134644a4c217d30731e69c')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
        
def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('div.item a')):
        if index ==10:
            return content
        print(data)
        title = data.find('img')['alt']
        link =  data['href']
        link2 = 'https:'+ data.find('img')['data-src']
        content+='{}\n{}\n{}\n'.format(title,link,link2)
    return content

def cnn():
    target_url = 'https://edition.cnn.com/2018/08/23/us/hurricane-lane-hawaii-wxc/index.html'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('.pg-rail-tall_wrapper'):
        print(data)
        title=data.find('img')['alt']
        link =  data['href']
        link2 = 'https:'+ data.find('img')['data-src']
        content+='{}\n{}\n{}\n'.format(title,link,link2)
    return content





@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    
    if event.message.text == "蘋果最新新聞":
       content=apple_news()
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
    return 0
    if event.message.text == "cnn":
       content=cnn()
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
    return 0
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

       
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105,
                   106,107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
                   125,126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(package_id='1',sticker_id=sticker_id
                                                        )
    line_bot_api.reply_message(event.reply_token,sticker_message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

