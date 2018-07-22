import argparse
import time
import numpy as np
import imutils
import cv2
import requests
from cv import imgCatcher
from cv import imageCls

from PIL import Image, ImageDraw, ImageFont

# 创建参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path of the video")
# 待检测目标的最小面积，该值需根据实际应用情况进行调整(原文为500)
ap.add_argument("-a", "--min-area", type=int, default=2000, help="minimum area size")
args = vars(ap.parse_args())    #@


def exe():
    # 如果video参数为空，则从自带摄像头获取数据
    if args.get("video") == None:
        camera = cv2.VideoCapture(0)
    # 否则读取指定的视频
    else:
        camera = cv2.VideoCapture(args["video"])
    # 开始之前先暂停一下,以便跑路(离开本本摄像头拍摄区域^_^)
    print("Ready?")
    time.sleep(1)
    print("Action!")
    # 初始化视频第一帧
    firstRet, firstFrame = camera.read()
    if not firstRet:
        print("Load video error!")
        exit(0)

    # 对第一帧进行预处理
    firstFrame = imutils.resize(firstFrame, width=500)  # 尺寸缩放，width=500
    gray_firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY) # 灰度化
    firstFrame = cv2.GaussianBlur(gray_firstFrame, (21, 21), 0) #高斯模糊，用于去噪

    counter = 0
    # 遍历视频的每一帧
    while True:
        (ret, frame) = camera.read()

        # 如果没有获取到数据，则结束循环
        if not ret:
            break

        # 对获取到的数据进行预处理
        frame = imutils.resize(frame, width=500)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        # cv2.imshow('video', firstFrame)
        # 计算第一帧和其他帧的差别
        frameDiff = cv2.absdiff(firstFrame, gray_frame)
        # 忽略较小的差别
        retVal, thresh = cv2.threshold(frameDiff, 25, 255, cv2.THRESH_BINARY)
        # 对阈值图像进行填充补洞
        thresh = cv2.dilate(thresh, None, iterations=2)
        image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if counter%10 == 0:
            firstFrame = imutils.resize(frame, width=500)  # 尺寸缩放，width=500
            gray_firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY) # 灰度化
            firstFrame = cv2.GaussianBlur(gray_firstFrame, (21, 21), 0) #高斯模糊，用于去噪
            # post image to server
            url = "http://10.20.192.100:8080/gettableinfo/"
            data = { 'name': 'nginx'}
            files = {'file': open("motion.jpg", 'rb')}
            response = requests.post(url, data=data, files=files)
            print("发送图片给服务器 .....")
        text = "Unoccupied"
        # 遍历轮廓
        for contour in contours:
            # if contour is too small, just ignore it
            if cv2.contourArea(contour) < args["min_area"]:
                continue
            # 计算最小外接矩形（非旋转）
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            filename = "motion.jpg"
            cv2.imwrite(filename, frame)
            # cv2读取图片
            img = cv2.imread(filename) # 名称不能有汉字
            cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # cv2和PIL中颜色的hex码的储存顺序不同
            pilimg = Image.fromarray(cv2img)
            # PIL图片上打印汉字
            draw = ImageDraw.Draw(pilimg) # 图片上打印
            font = ImageFont.truetype("simhei.ttf", 20, encoding="utf-8") # 参数1：字体文件路径，参数2：字体大小
            prob, tag = imageCls.what_is_img(filename)   
            text = "这由%.3f的可能是一个%s"%(prob, tag)
            draw.text((0, 0), text, (255, 0, 0), font=font)     
            # PIL图片转cv2 图片
            cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
            cv2.imshow("photo", cv2charimg)
        cv2.putText(frame, "Room Status: {}".format(text), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

        # 处理按键效果
        key = cv2.waitKey(60) & 0xff
        if key == 27:   # 按下ESC时，退出
            break
        elif key == ord(' '):   # 按下空格键时，暂停
            cv2.waitKey(0)
        time.sleep(1)
        counter += 1

    # 释放资源并关闭所有窗口
    camera.release()
    cv2.destroyAllWindows()