from flask import Flask, request, abort,render_template
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, TemplateSendMessage,ButtonsTemplate,URIAction,QuickReplyButton,QuickReply
)

import time
import math
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
import random

from datetime import datetime as dt

import urllib.request, urllib.error

from apiclient.discovery import build
import urllib.parse
import re, requests
DEVELOPER_KEY = "AIzaSyDFBCD1FCBGX2_Wdt2jhedKW13y3E0QlZw"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
def checkURL(url):
    try:
        f = urllib.request.urlopen(url)
        print ("OK:" + url )
        f.close()
        return True
    except Exception as e:
        print (str(e))
        print ("NotFound:" + url)
        return False

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

'''

conn = get_connection()

cur = conn.cursor()


sql = "insert into retasudb values('user_id','Aくん','100')"

cur.execute("insert into botdb values({id},'{user_id}','{name}','{point}')".format(id=2,user_id='user_id2'+'Aくん2',name='Aくん',point='200'))

cur.execute("UPDATE botdb SET point = '200' WHERE id='2';")

cur.execute("UPDATE botdb SET point = '200' WHERE id='6039';")

cur.execute('SELECT * FROM botdb')



cur = connection.cursor()
cur.execute("ROLLBACK")
conn.commit()

cur.execute('SELECT * FROM botdb')

row_ = []

for row in cur:
    if 'user_id2Aくん' in row:
        ok = row[3]
    else:
        pass
    row_.append(row)

print(ok)

print(row_)


cur.execute("UPDATE botdb SET point = '{point}' WHERE id='{dbID}';".format(point='250',dbID='6039'))


'''


set_ = 2

app = Flask(__name__)

stoptime = 0

stoppoint = 0

setting_ = {}
'''
setting_ = {
    user_id:{
        'use':True,
        'name':'name',
        'point':0,
    	'time':0,
    	'timepoint':0,
        'ID':'',
    }
}
'''
setting2 = {
	'setting1':False,
	'setting2':False,
	'setting3':False,
	'setting4':False,
	'setting5':False,
	'setting6':False,
	'setting7':False,
	'setting8':False,
	'setting9':False,
	'setting10':False,
}



Time = {
    'count':0,
    'pointcount_1':0,
    'pointcount_2':0,
    'pointcount2_1':0,
    'pointcount2_2':0,
}
'''
Time = {
    user_id:{
        'count':0,
        'pointcount_1':0,
        'pointcount_2':0,
        'pointcount2_1':0,
        'pointcount2_2':0
        }
}


date = {
    'ID':{'point':0}
}
'''
date = {}
setting_youtube = {}
pdate = {
    'save': True,
    'date': '',
    'point':0
    }


def pick_up_vid(url):
  pattern_watch = 'https://www.youtube.com/watch?'
  pattern_short = 'https://youtu.be/'


  if re.match(pattern_watch,url):
    yturl_qs = urllib.parse.urlparse(url).query
    vid = urllib.parse.parse_qs(yturl_qs)['v'][0]
    return vid

    # 短縮URLのとき
  elif re.match(pattern_short,url):
    # "https://youtu.be/"に続く11文字が動画ID
    vid = url[17:28]
    return vid


def Flex(date):
    payload = {'id': pick_up_vid(date[0]), 'part': 'contentDetails,statistics,snippet', 'key': DEVELOPER_KEY}
    l = requests.Session().get('https://www.googleapis.com/youtube/v3/videos', params=payload)
    resp_dict = json.loads(l.content)
    title = resp_dict['items'][0]['snippet']['title']
    sum_ = resp_dict['items'][0]['snippet']['thumbnails']['standard']['url']
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    },
    "url": sum_
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": title,
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "md",
        "contents": [
          {
            "type": "icon",
            "size": "sm",
            "url": "https://www.flaticon.com/svg/static/icons/svg/126/126473.svg"
          },
          {
            "type": "text",
            "text": date[2],
            "size": "sm",
            "color": "#999999",
            "margin": "md",
            "flex": 0
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "コメント",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": date[1],
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "ジャンル",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": date[4],
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "動画を見る",
          "uri": date[0]
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "いいねをつける",
          "text": "いいね！"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}

    return data



def youtube_set(url,text,point,point_id,ctg):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM ydb')
    cur.execute("insert into ydb values('{url}','{text}','{point}','{point_id}','{ctg}')".format(url=url,text=text,point=point,point_id=point_id,ctg=ctg))
    conn.commit()
    return True


def geturl():
    point = None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM ydb')
    URL_list = []
    for row in cur:
        if 'youtu.be' in row[0] or 'youtube.com' in row[0]:
            URL_list.append(row)
        else:
            pass
    print(URL_list)
    return random.choice(URL_list)

def getdata(url):
    point = None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM ydb')
    for row in cur:
        if url == row[0]:
            print(row)
            return row

def IDcheck(ID):
    point = None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM ydb')
    '''
    with open('date.json','r') as f:
        date = json.load(f)
    '''

    for row in cur:
        if ID in row:
            return row[1]

def seve(ID,text):
    try:
        #namecheck(ID,text)
        print('ok2')
        print(setting_[ID]['dbID'])
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM ydb')
        #text = setting_[ID]['text']
        for row in cur:
            if ID in row:
                dbID = row[0]
                print('ok3')
                print(text)
                print(dbID)
                cur.execute("UPDATE ydb SET name = '{text}' WHERE url='{url}';".format(text=ID,url=URL))
                conn.commit()
                print('ok3-2')
                return text
        cur.execute("UPDATE ydb SET name = '{name}' WHERE user_id='{user_id}';".format(name=text,user_id=ID))
        conn.commit()
        print('ok4')
    except Exception as e:
        print (str(e))
        return namecheck(user_id,text)
    '''


    with open('date.json','r') as f:
        date = json.load(f)
    date[ID][setting_[ID]['name']] = date[ID][setting_[ID]['name']] + setting_[ID]['point2']
    with open('date.json','w') as f:
        json.dump(date, f)
    '''

def seve2(ID,URL):
    #ID=ユーザーID URL=youtube_url
    try:
        print('ok2')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM ydb')
        for row in cur:
            if ID in row:
                print(row)
                dbID = row[0]
                print('ok3')
                print(dbID)
                cur.execute("UPDATE ydb SET text = '{text}' WHERE url='{url}';".format(text=ID,url=URL))
                conn.commit()
                print('ok3-2')
                return
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        cur.execute("insert into ydb values('{url}','{text}','{point}','{point_id}','{ctg}')".format(url=ID,text=URL,point='0',point_id='0',ctg='0'))
        conn.commit()
        print('ok4')
        return
    except Exception as e:
        print (str(e))
        return

def seve3(URL,id_list):
    try:
        print('ok2-')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM ydb')
        for row in cur:
            if ID in row:
                print(row)
                dbID = row[0]
                print('ok3-')
                print(dbID)
                cur.execute("UPDATE ydb SET point_id = '{id_list}' WHERE url='{url}';".format(id_list=id_list,url=URL))
                conn.commit()
                print('ok3-2-')
                return
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        #cur.execute("insert into ydb values('{url}','{text}','{point}','{point_id}','{ctg}')".format(url=ID,text=URL,point='0',point_id='0',ctg='0'))
        #conn.commit()
        print('error')
        return
    except Exception as e:
        print (str(e))
        return

def seve4(URL,point):
    try:
        print('-ok2-')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM ydb')
        for row in cur:
            if ID in row:
                print(row)
                dbID = row[0]
                print('-ok3-')
                print(dbID)
                cur.execute("UPDATE ydb SET point = '{point}' WHERE url='{url}';".format(point=point,url=URL))
                conn.commit()
                print('-ok3-2-')
                return
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        #cur.execute("insert into ydb values('{url}','{text}','{point}','{point_id}','{ctg}')".format(url=ID,text=URL,point='0',point_id='0',ctg='0'))
        #conn.commit()
        print('error')
        return
    except Exception as e:
        print (str(e))
        return


def like(ID,data):
    print(point)
    print(data[3])
    list_ = data[3].split(',')
    if ID in list_:
        return False
    else:
        list_.append(ID)
        str_ = ','.join(list_)
        point = int(data[2]) + 1
        seve3(data[0],str_)
        seve4(data[0],str(point))
        return True


#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = 'zXRwETgD58JHDKQkSD6YvdcnT8NEJWPtE2+Ua1QTt4E+5tRzu4lW8+nhMlVMU1xeHlpDtQAzfuq/qIRJ4OAYcGa3QyO30eW7xAgh0mlTcPHVqLOQut08U2e1FoYTWd/EUu9bb1P3WS6jSa7oCwoLQwdB04t89/1O/w1cDnyilFU='
#os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = 'bdc23bca4c8508095ee101b4a6765057'
#os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def hello_world():
    return "hello world!"


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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global set_
    global stoptime
    global stoppoint
    msg_from = event.reply_token
    msg_text = event.message.text
    user_id = event.source.user_id
    '''if msg_text == '設定する':
        items = {'items': [{'type': 'action','action': {'type': 'message','label': '貯める','text': '貯める'}},{'type': 'action','action': {'type': 'message','label': '使う','text': '使う'}}]}
        line_bot_api.reply_message(msg_from,TextSendMessage(text='まずは貯めるのか使うのかを教えてね！',quick_reply=items))
        setting_[user_id] = {'use':True,'name':'name','point':0,'time':0,'timepoint':0,'ID':'','point2':0,'dbID':0}
        setting_[user_id]['ID'] = user_id
        Time[user_id] = {'count':0,'pointcount_1':0,'pointcount_2':0,'pointcount2_1':0,'pointcount2_2':0}
        setting2[user_id] = {'setting1':False,'setting2':False,'setting3':False,'setting4':False,'setting5':False,'setting6':False,'setting7':False,'setting8':False,'setting9':False,'setting10':False,}
        set_ = 2
'''
    if msg_text == '布教する':
        line_bot_api.reply_message(msg_from,TextSendMessage(text='まずは布教したいYoutubeの動画のリンクを送ってね！'))
        setting_[user_id] = {'use':True,'name':'name','point':0,'time':0,'timepoint':0,'ID':'','point2':0,'dbID':0}
        setting_[user_id]['ID'] = user_id
        Time[user_id] = {'count':0,'pointcount_1':0,'pointcount_2':0,'pointcount2_1':0,'pointcount2_2':0}
        setting2[user_id] = {'setting1':False,'setting2':False,'setting3':False,'setting4':False,'setting5':False,'setting6':False,'setting7':False,'setting8':False,'setting9':False,'setting10':False,}
        set_ = 2
        setting2[user_id]['setting1'] = True
        return

    if msg_text == 'ゲットする':
        url = geturl()
        flex_ = Flex(url)
        seve2(user_id,url[0])
        flex = {"type": "flex","altText": "YouTubeリンク","contents":flex_}
        line_bot_api.reply_message(msg_from,messages=container_obj)
        return

    if msg_text == 'いいね！':
        url = IDcheck(user_id)
        data = getdata(url)
        hoge = like(user_id,data)
        if hoge == True:
            line_bot_api.reply_message(msg_from,TextSendMessage(text="いいねを押したよ！"))
        if hoge == False:
            line_bot_api.reply_message(msg_from,TextSendMessage(text="いいねを押せなかったよ！\nいいねは1回しか押せないよ！"))
        return


#    if 'メッセージ:' in msg_text:
#        #namecheck(user_id,'test')
#        msg_text_ = msg_text.replace("メッセージ:","")
#        line_bot_api.reply_message(msg_from,TextSendMessage(text='送信したよ！'))
#        line_bot_api.reply_message("U76d18383a9b659b9ab3d0e43d06c1e78",TextSendMessage(text=msg_text_))


    else:
        try:
            if setting2[user_id]['setting1'] == True and user_id == setting_[user_id]['ID']:
                setting2[user_id]['setting1'] = False
                try:
                    if 'youtu.be' in msg_text or 'youtube.com' in msg_text:
                        print('url OK')
                        URL = msg_text
                        setting_youtube[user_id] = {'url':URL,'text':'','ctg':''}
                        setting2[user_id]['setting2'] = True
                        line_bot_api.reply_message(msg_from,TextSendMessage(text='URLを設定したよ！\n次はURLの動画についてのコメントを送信してね！！'))
                        return
                except Exception as e:
                    print (str(e))
                    return
        except Exception as e:
                    print (str(e))
                    line_bot_api.reply_message(msg_from,TextSendMessage(text='失敗！'))
                    return
        if setting2[user_id]['setting2'] == True and user_id == setting_[user_id]['ID']:
            try:
                print('ok-12')
                setting_youtube[user_id]['text'] = msg_text
                setting2[user_id]['setting2'] = False
                setting2[user_id]['setting3'] = True
                items = {'items': [{'type': 'action','action': {'type': 'message','label': '音楽','text': '音楽'}},{'type': 'action','action': {'type': 'message','label': 'おもしろ','text': 'おもしろ'}},{'type': 'action','action': {'type': 'message','label': 'VTuber','text': 'VTuber'}}]}
                line_bot_api.reply_message(msg_from,TextSendMessage(text='コメントを設定できたよ！\n次は動画のカテゴリーを決めて送信してね！\nカテゴリーは好きに作れるよ！\n\n迷ったときは下のボタンからも送信できるよ！',quick_reply=items))
                return
            except Exception as e:
                print (str(e))
                line_bot_api.reply_message(msg_from,TextSendMessage(text='失敗！'))
                return

        if setting2[user_id]['setting3'] == True and user_id == setting_[user_id]['ID']:
            try:
                print('ok-13')
                setting2[user_id]['setting3'] = False
                setting_youtube[user_id]['ctg'] = msg_text
                id_list = ['test']
                id_list.append(user_id)
                id_list_str = ','.join(id_list)
                youtube_set(setting_youtube[user_id]['url'],setting_youtube[user_id]['text'],"0",id_list_str,setting_youtube[user_id]['ctg'])
                line_bot_api.reply_message(msg_from,TextSendMessage(text='アップできたよ！'))
                return
            except Exception as e:
                print (str(e))
                line_bot_api.reply_message(msg_from,TextSendMessage(text='失敗！'))
                return

        else:
            items = {'items': [{'type': 'action','action': {'type': 'message','label': '設定する','text': '設定する'}},{'type': 'action','action': {'type': 'message','label': 'メッセージ送信','text': 'メッセージ送信'}}]}
            line_bot_api.reply_message(msg_from,TextSendMessage(text='表示する文字を設定したいときは\n「設定する」\nと送信してね！\n\nひとこと連絡を使う場合は\n「メッセージ送信」\nと送信してね！\n\n下のボタンからも送信できるよ！',quick_reply=items))





if __name__ == "__main__":
#    app.run()
    port =  int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
