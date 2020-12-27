from transitions.extensions import GraphMachine

from utils import send_text_message
from linebot.models import MessageTemplateAction
from utils import send_button_message, send_image_message
from catchdata import cloudpicture, airpicture, today, week
from flask import Flask, jsonify, request, abort, send_file

#global variable
city = "嘉義市"

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state(self, event):
        text = event.message.text
        return text.lower() == "hi"

    def on_enter_state(self, event):
        title = "請選擇功能"
        text = "請依照需求點選功能"
        btn = [
            MessageTemplateAction(
                label = "今天天氣",
                text = "今天天氣"
            ),
            MessageTemplateAction(
                label = "今天空氣品質",
                text = "今天空氣品質"
            ),
            MessageTemplateAction(
                label = "一周天氣預報",
                text = "一周天氣預報"
            ),
            MessageTemplateAction(
                label = "衛星雲圖",
                text = "衛星雲圖"
            )
        ]
        url = 'https://i.imgur.com/tyOAIAG.png'
        send_button_message(event.reply_token, title, text, btn, url)
        
    
    def is_going_to_todayweather(self, event):
        text = event.message.text
        if text == "今天天氣":
            return True
        return False
    
    def on_enter_todayweather(self, event):
        print("I'm entering todayweather")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您的城市")

    def is_going_to_city(self, event):
        global city
        temp = event.message.text
        if temp[0] == "台":
            tmp = "臺" + temp[1:]
            temp = tmp
        if temp == ("宜蘭縣" or "桃園市" or "新竹縣" or "苗栗縣" or "彰化縣" or "南投縣" or "雲林縣" or "嘉義縣" or "屏東縣" or "臺東縣" or "花蓮縣" or "澎湖縣" or "基隆市" or "新竹市" or "嘉義市" or "臺北市" or "高雄市" or "新北市" or "臺中市" or "臺南市" or "連江縣" or "金門縣"):
            city = temp
            return True
        else:
            return False
    
    def on_enter_city(self, event):
        print("I'm entering city")
        global city
        reply_token = event.reply_token
        send_text_message(reply_token, today(city))
        #self.go_state(event)
        self.go_back()
    
    def is_going_to_picture(self, event):
        text = event.message.text
        if (text == "衛星雲圖"):
            return True
        return False
    
    def on_enter_picture(self, event):
        print("I'm entering picture")
        reply_token = event.reply_token
        send_image_message(reply_token, cloudpicture())
        #self.go_state(event)
        self.go_back()

    def is_going_to_air(self, event):
        text = event.message.text
        if (text == "今天空氣品質"):
            return True
        return False
    
    def on_enter_air(self, event):
        print("I'm entering air")
        reply_token = event.reply_token
        send_image_message(reply_token, airpicture())
        #self.go_state(event)
        self.go_back()

    def is_going_to_weekweather(self, event):
        text = event.message.text
        if text == "一周天氣預報":
            return True
        return False
    
    def on_enter_weekweather(self, event):
        print("I'm entering weekweather")

        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入您的城市")

    def is_going_to_weekcity(self, event):
        global city
        temp = event.message.text
        if temp[0] == "台":
            tmp = "臺" + temp[1:]
            temp = tmp
        if temp == ("宜蘭縣" or "桃園市" or "新竹縣" or "苗栗縣" or "彰化縣" or "南投縣" or "雲林縣" or "嘉義縣" or "屏東縣" or "臺東縣" or "花蓮縣" or "澎湖縣" or "基隆市" or "新竹市" or "嘉義市" or "臺北市" or "高雄市" or "新北市" or "臺中市" or "臺南市" or "連江縣" or "金門縣"):
            city = temp
            return True
        else:
            return False
    
    def on_enter_weekcity(self, event):
        print("I'm entering city")
        try:
            global city
            reply_token = event.reply_token
        #week(city)
        #send_image_message(reply_token, "https://5be4cb182235.ngrok.io/show-week")
            send_text_message(reply_token, week(city))
        #self.go_state(event)
            self.go_back()    
        except Exception as ex:
            print(ex)
        

    def is_going_to_graph(self, event):
        text = event.message.text
        return text.lower() == "graph"
    
    def on_enter_graph(self, event):
        print("I'm entering graph")
        reply_token = event.reply_token
        send_image_message(reply_token, "https://weatherobot.herokuapp.com/show-fsm")
        self.go_back()
    