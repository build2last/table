""" 餐桌场景识别 service Framework

1. 通用识别——识别出物品的类别
2. 菜品识别——识别出菜品的名称和卡路里含量

"""

__author__ = "LiuKun"
__python__ = 3.6
__version__ = 0.1

import hashlib
import xml.etree.ElementTree as ET
import time
import json
from flask import Flask, request, make_response, jsonify, Response
from cv import imageCls
from cv import imgCatcher

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return '我是终端!'


@app.route('/getEatList', methods=['GET'])
def get_eat_list():
  if request.method == 'GET':                # 如果是get方法--从服务器请求数据
    eat_hist = {
      "tid":"123456789",
      "dishes":[
        {"name":"冰激凌", "time":"2018-07-21 19:00"},
        {"name":"可口可乐", "time":"2018-07-21 19:32"}
      ]
    }
    return jsonify(eat_hist) #jsonify(imageCls.shoot_now())


@app.route('/getdish', methods=['GET'])
def getdish():
  if request.method == 'GET':                # 如果是get方法--从服务器请求数据
    meals = {
      "tid":"123456789",
      "meals":[
        {
            "mid":"1",
            "begin_time":"2018-07-21 19:00",
            "end_time":"2018-07-21 19:32",
            "dishes":
              [
                {"name":"冰淇淋", "calorie":127},
                {"name":"可口可乐", "calorie":100}
              ]
            ,
            "eat_cal": 220
        },
        {
            "mid":"2",
            "begin_time":"2018-07-22 7:00",
            "end_time":"2018-07-22 7:32",
            "dishes":
              [
                {"name":"小米粥", "calorie":37},
                {"name":"芒果奶", "calorie":50}
              ],
            "eat_cal": 87
        }
      ]
    }
    return jsonify(meals) #jsonify(imageCls.shoot_now())


@app.route('/info', methods=['GET', 'POST'])
def getinfo():
    if request.method == 'GET':                 # 如果是get方法--从服务器请求数据
      img_time = request.args.get('time', '')
      if img_time == "latest":
          img_path = imgCatcher.get_image(save_to="shoot")
      elif img_time == "test":
          img_path = "shoot/mpdf.jpg"
      info = imageCls.query_img(img_path)
    import pprint
    pprint.pprint(info)
    return jsonify(info)

import uuid
@app.route('/img', methods=['GET', 'POST'])
def getimg():
    if request.method == 'GET':                 # 如果是get方法--从服务器请求数据
      img_time = request.args.get('time', '')
      if img_time == "latest":
          img_path = imgCatcher.get_image(save_to="shoot", now=True)
          image = open(img_path, "rb")
      else:
          image = open("shoot/mpdf.jpg", "rb")
      resp = Response(image.read(), mimetype="image/jpeg")
      return resp
    else:
        file = request.files['file']
        if file:
            #因为上次的文件可能有重名，因此使用uuid保存文件
            file_name = str(uuid.uuid4()) + '.jpg'
            file.save(file_name)
            return "over"


from multiprocessing import Process
import winsound

def alert_info(info):
	import win32com.client
	speak = win32com.client.Dispatch('SAPI.SPVOICE')
	speak.Speak(info)


@app.route('/alert', methods=['GET', 'POST'])
def get_alert():
    if request.method == 'GET':                 # 如果是get方法--从服务器请求数据
      remind = request.args.get('remind', '发现过敏原芒果!')
      for _ in range(3):
        winsound.Beep(800, 500)
      t = Process(target=alert_info, args=(remind,))
      t.start()
      t.join()
      return "警告已播放"


if __name__ == '__main__':
    app.run('0.0.0.0',port=8080)