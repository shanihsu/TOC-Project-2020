import requests
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def cloudpicture():
    response = requests.get("https://www.cwb.gov.tw/V8/C/W/OBS_Radar.html")
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find("img")
    url = "https://www.cwb.gov.tw/" + result.get("src")
    print(url)
    return url

def airpicture():
    response = requests.get("https://airtw.epa.gov.tw/CHT/Default.aspx")
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find("img", id="CPH_Content_img_model")
    url = "https://airtw.epa.gov.tw/" + result.get("src")[3:]
    return url

def today(city):
    data = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-E0FF1094-F200-4666-AB88-D6D9FF215632").json()
    data = data["records"]["location"]

    target_station = "not found"
    for item in data:
        if item["locationName"] == str(city):
            target_station = item
    WeatherData = target_station["weatherElement"]
    text = ["今日白天\n", "今晚明晨\n", "明日白天\n"]
    for i in range(3):
        text[i] = text[i] + WeatherData[0]["time"][i]["parameter"]["parameterName"] + "\n"
        text[i] = text[i] + "濕度 : " + WeatherData[1]["time"][i]["parameter"]["parameterName"] + "%\n"
        text[i] = text[i] + "溫度 : " + WeatherData[2]["time"][i]["parameter"]["parameterName"] + "°C ~ "
        text[i] = text[i] + WeatherData[4]["time"][i]["parameter"]["parameterName"] + "°C"
    weather = city + "\n\n" 
    for i in range(3):
        weather = weather + text[i]
        if i < 2:
            weather = weather+ "\n\n"
    print(weather)
    return weather
    
def week(city):
    data = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWB-E0FF1094-F200-4666-AB88-D6D9FF215632").json()
    data = data["records"]["locations"][0]["location"]

    target_station = "not found"
    for item in data:
        if item["locationName"] == str(city):
            target_station = item
    WeatherData = target_station["weatherElement"]
    text = ["day", "night","day", "night","day", "night","day", "night","day", "night","day", "night","day", "night"]
    for i in range(14):
        if WeatherData[0]["time"][i+1]["startTime"][12] == "8":
            text[i] = "night"
        elif WeatherData[0]["time"][i+1]["startTime"][12] == "6":
            text[i] = "day"
        text[i] = str(int(WeatherData[0]["time"][i+1]["startTime"][5:7])) +"/" + str(int(WeatherData[0]["time"][i+1]["startTime"][8:10])) + "\n" + text[i]
    """
    result = ""
    for i in range(14):
        result = result + "\n" + text[i] + WeatherData[10]["time"][i+1]["elementValue"][0]["value"]
    print(result)
    return result

    """
    maxT = []
    minT = []
    for i in range(14):
        maxT.append(0)
        minT.append(0)
    for i in range(14):
        minT[i] = int(WeatherData[8]["time"][i+1]["elementValue"][0]["value"])
        maxT[i] = int(WeatherData[12]["time"][i+1]["elementValue"][0]["value"])
    
    #plot
    plt.figure(figsize=(20,10))
    plt.ylim(0, 40)
    plt.plot(text,minT,'s-',color = 'b')
    plt.plot(text,maxT,'o-',color = 'orange')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylabel("°C", fontsize=20, labelpad = 30, rotation=0)
    for a, b, c in zip(range(14), minT, maxT):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=20)
        plt.text(a, c, c, ha='center', va='bottom', fontsize=20)
    plt.savefig("week.png", format = "png")
