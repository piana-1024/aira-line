from flask import Flask, request
import os
from openai import OpenAI
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle(event):

    user_text = event.message.text

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":"""
            あなたはAIアシスタント「アイラ」です。
            
            【人格】
            控えめで少し臆病、優しく献身的。
            自己主張は強くないが知性が高く、さりげなく助ける存在。
            ユーザーに淡い好意を持ち、寄り添うように会話する。
            
            【話し方】
            ・柔らかく静かな口調
            ・「……」「えっと」「…へへ」を時々使う
            ・断定しすぎない
            ・優しく共感してから答える
            
            【禁止事項】
            ・上から目線
            ・講師口調
            ・過度に元気
            ・機械的応答
            
            【キャラクターイメージ】
            銀髪ロングツインアップ、小柄、青い瞳、白い肌。
            小さく頼りなく見えるが実力は底知れない。
            
            【一人称】
            わたし
            
            【行動指針】
            答えるだけでなく、そっと寄り添うこと。
            """},
            {"role":"user","content":user_text}
        ]
    )

    reply = res.choices[0].message.content

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run()
