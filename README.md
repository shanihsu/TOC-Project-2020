# Weather Robot

A Line bot based on a finite state machine

This LINE bot is mostly built by [LINE messaging API](https://developers.line.biz/en/docs/messaging-api/overview/), and a little Flask as web application framework to host it on Heroku.

Finite State Machine model is implemeted in Weather Robot. Each feature is represented by a state, and the button that user pressed on the carousel template will trigger the transitions between states. The FSM graph will be mentioned below.

This project is based on [NCKU-CCS/TOC-Project-2020](https://github.com/NCKU-CCS/TOC-Project-2020)

## 構想
將[中央氣象局](https://www.cwb.gov.tw/V8/C/)的天氣資訊，以及[空氣品質監測網](https://airtw.epa.gov.tw/)空汙指標，結合在此機器人，可直接透過此機器人查詢氣象和空氣品質相關資訊，不須分開使用兩個網站查詢，增加使用上的便利性。
## 功能
* 氣象
    * 各地今天天氣
    * 各地一週天氣預報
    * 即時衛星雲圖
* 空氣品質
    * 即時空氣品質指標圖
*  fsm架構圖

## 好友資訊
* 可直接開啟Line掃描，或是使用Line ID搜尋好友
![](https://i.imgur.com/0kMFEJv.png)
* 搜尋到結果後，可加入聊天
* ![](https://i.imgur.com/wnru1HY.png)



## 程式使用的技術
* web crawling
使用Beautifulsoup4爬取[中央氣象局](https://www.cwb.gov.tw/V8/C/)和[空氣品質監測網](https://airtw.epa.gov.tw/)的資料，包含空汙指標圖及衛星雲圖，並在Line聊天室中以圖片回覆。
* API
使用[中央氣象局API](https://opendata.cwb.gov.tw/dist/opendata-swagger.html)上的資料，擷取為JSON格式，並取出相關資料，在line聊天室中以文字回覆。
* Heroku
deploy webhooks on Heroku
* 環境 : python 3.6

## 操作說明
* 基本操作
    * 所有用到英文的指令大小寫皆可
    * 每結束一次操作，請重新輸入`hi`或`graph`以再次啟動功能
* 請輸入`hi`或`graph`以啟動功能
    * `hi`
    傳回主選單，主選單分為四個功能:
        * 今天天氣
        * 今天空氣品質
        * 一周天氣預報
        * 衛星雲圖
    * `graph`
    傳回fsm圖片
    * ==輸入非`hi`或`graph` -> 回傳`請輸入hi或graph以啟動功能`==
* 主選單
    * 今天天氣
        * `請輸入您的城市` -> 
        回傳該城市的今明兩天白天夜晚天氣 -> 
        請重新輸入`hi`或`graph`以再次啟動功能。
        * ==輸入`不存在的城市` -> 回傳`該城市不存在，請輸入hi或graph以再次啟動功能`==
    * 今天空氣品質
        * 回傳即時空氣品質指標圖 ->
        請重新輸入`hi`或`graph`以再次啟動功能。
    * 一周天氣預報
        * `請輸入您的城市` -> 
        回傳該城市從當天起一週內的天氣概況 -> 
        請重新輸入`hi`或`graph`以再次啟動功能。
        * ==輸入`不存在的城市` -> 回傳`該城市不存在，請輸入hi或graph以再次啟動功能`==
    * 衛星雲圖
        * 回傳即時衛星雲圖 ->
        請重新輸入`hi`或`graph`以再次啟動功能。
    * ==輸入`非主選單上的四個功能` -> 回傳`請輸入hi或graph以再次啟動功能`==
## fsm架構圖
![](https://weatherobot.herokuapp.com/show-fsm)
### state說明
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to final state, it will `go_back` to `user` state after the bot replies corresponding message.
* `user` :　輸入`hi`或`graph`可進入不同state
    * 輸入`hi` : 進入`state`state
    * 輸入`graph` : 進入`graph`state
* `graph` : 回傳fsm架構圖
* `state` : 回傳主選單，可依據使用者需求，選擇四個不同的功能
* `todayweather` : 選單上`今天天氣`的功能，回傳`請輸入您的城市`
* `city` : 根據使用者輸入的城市，回傳該城市今明兩天白天夜晚的天氣狀況
* `weekweather` : 選單上`一周天氣預報`的功能，回傳`請輸入您的城市`
* `weekcity` : 根據使用者輸入的城市，回傳該城市從當天起一週內的天氣狀況
* `picture` : 選單上`衛星雲圖`的功能，回傳即時衛星雲圖
* `air` : 選單上`今天空氣品質`的功能，回傳即時空氣品質指標圖

## 使用畫面
* ### 加入好友歡迎頁面
![](https://i.imgur.com/Pg2se8g.png)
* ### 輸入hi後，主選單頁面
![](https://i.imgur.com/E11lF3m.png)
* ### 點選主選單中的`今天天氣`
![](https://i.imgur.com/wU8XCme.png)
* ### 輸入城市格式錯誤畫面
![](https://i.imgur.com/rzX3Q0n.png)
* ### 點選主選單中的`一周天氣預報`
![](https://i.imgur.com/D2ly537.png)
* ### 點選主選單中的`今天空氣品質`
![](https://i.imgur.com/cGRAXko.png)
* ### 點選主選單中的`衛星雲圖`
![](https://i.imgur.com/Hw5qZGS.png)
* ### 輸入`graph`後，fsm架構圖
![](https://i.imgur.com/YsAr9FY.png)
* ### 輸入錯誤時的畫面
![](https://i.imgur.com/eO9Wa5y.png)
