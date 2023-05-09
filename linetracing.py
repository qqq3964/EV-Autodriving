#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import matplotlib.pyplot as plt
from os.path import sep
import rospy
from std_msgs.msg import Int8MultiArray, Int8
from collections import deque

minpix = 5

lane_bin_th = 145

mode=0

def mode_callback(msg):
    global mode
    mode=msg.data

def warp_process_image(lane, current):
    nwindows=10
    margin = 50
    global minpix
    global lane_bin_th

    leftx_current, rightx_current = current

    window_height = 48
    nz = lane.nonzero()

    left_lane_inds = []
    right_lane_inds = []
    
    lx, ly, rx, ry = [], [], [], []

    out_img = lane
    out_img = np.dstack((lane, lane, lane))*255

    for window in range(nwindows):

        win_yl = lane.shape[0] - (window+1)*window_height
        win_yh = lane.shape[0] - window*window_height

        win_xll = leftx_current - margin
        win_xlh = leftx_current + margin
        win_xrl = rightx_current - margin
        win_xrh = rightx_current + margin

        cv2.rectangle(out_img,(win_xll,win_yl),(win_xlh,win_yh),(0,255,0), 2) 
        cv2.rectangle(out_img,(win_xrl,win_yl),(win_xrh,win_yh),(0,255,0), 2) 

        good_left_inds = ((nz[0] >= win_yl)&(nz[0] < win_yh)&(nz[1] >= win_xll)&(nz[1] < win_xlh)).nonzero()[0]
        good_right_inds = ((nz[0] >= win_yl)&(nz[0] < win_yh)&(nz[1] >= win_xrl)&(nz[1] < win_xrh)).nonzero()[0]

        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)

        if len(good_left_inds) > minpix:
            leftx_current = np.int(np.mean(nz[1][good_left_inds]))
        if len(good_right_inds) > minpix:        
            rightx_current = np.int(np.mean(nz[1][good_right_inds]))

        if leftx_current >=320:
            leftx_current=rightx_current
        if rightx_current<=320:
            rightx_current=leftx_current

        lx.append(leftx_current)
        ly.append((win_yl + win_yh)/2)

        rx.append(rightx_current)
        ry.append((win_yl + win_yh)/2)

    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)

    # left_fit = np.polyfit(nz[0][left_lane_inds], nz[1][left_lane_inds], 2)
    # right_fit = np.polyfit(nz[0][right_lane_inds] , nz[1][right_lane_inds], 2)
    
    lfit = np.polyfit(np.array(ly),np.array(lx),2)
    rfit = np.polyfit(np.array(ry),np.array(rx),2)

    out_img[nz[0][left_lane_inds], nz[1][left_lane_inds]] = [255, 0, 0]
    out_img[nz[0][right_lane_inds] , nz[1][right_lane_inds]] = [0, 0, 255]
    center_x_0,center_y_0 = (lx[0]+rx[0])/2,(ly[0]+ry[0])/2
    center_x_2,center_y_2 = (lx[2]+rx[2])/2,(ly[2]+ry[2])/2

    if (center_x_2 - center_x_0) > 0:
        if center_x_2 != center_x_0:
            slope = (center_y_0 - center_y_2)/(center_x_2 - center_x_0)
            angle = np.rad2deg(np.arctan(slope))-90
        else:
            slope = 1000
            angle = np.rad2deg(np.arctan(slope))-90
    else:
        if center_x_2 != center_x_0:
            slope = (center_y_0 - center_y_2)/(center_x_2 - center_x_0)
            angle = np.rad2deg(np.arctan(slope))+90
        else:
            slope = 1000
            angle = np.rad2deg(np.arctan(slope))-90

    #return left_fit, right_fit
    return out_img, angle, center_x_2




# 노트북 화각
# def perspective_warp(img,
#                      src=np.array([[int(640*0.25), 480//2+120],[int(640*0.75),480//2+120],[640,480],[0,480]],dtype=np.float32),
#                      dst=np.array([[0,0],[640,0],[640,480],[0,480]],dtype=np.float32)):
#     matrix = cv2.getPerspectiveTransform(src,dst)
#     warped_img = cv2.warpPerspective(img,matrix,(640,480))

#     return warped_img

# 웹캡 화각
def perspective_warp(img,
                     src=np.array([[int(640*0.2), 480//2],[int(640*0.8),480//2],[640,480],[0,480]],dtype=np.float32),
                     dst=np.array([[0,0],[640,0],[640,480],[0,480]],dtype=np.float32)):
    matrix = cv2.getPerspectiveTransform(src,dst)
    warped_img = cv2.warpPerspective(img,matrix,(640,480))

    return warped_img

def region_of_interest(img, color3=(255,255,255), color1=255): # ROI 셋팅
    # 480,640
    y, x = img.shape[0],img.shape[1]
    # 좌아래 좌상단 우상단 우아래
    # vertices = np.array([[(0,height),(0, height//2+120), (width, height//2+120), (width,height)]], dtype=np.int32)
    vertices = np.array(
        [[0, int(y)], [0, 0], [int(0.5*x), 0], [int(0.5*x), int(y//2)], [int(0.45*x),int(y//2)],[int(0.45*x),int(y)],[int(0.55*x), int(y)],[int(0.55*x),int(y//2)],[int(0.5*x),int(y//2)], [int(0.5*x), 0],[int(x), 0], [int(x), int(y)]])
    mask = np.zeros_like(img) # mask = img와 같은 크기의 빈 이미지
    
    if len(img.shape) > 2: # Color 이미지(3채널)라면 :
        color = color3
    else: # 흑백 이미지(1채널)라면 :
        color = color1
        
    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움 
    cv2.fillPoly(mask, np.int32([vertices]), color)
    
    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image

def weighted_img(img, initial_img, a=0.8, b=1., c=1.): # 두 이미지 operlap 하기
    return cv2.addWeighted(initial_img, a, img, b, c)

def main():
    # ROS callback 함수
    # ROS 루프 실행
    queue =deque([0,0,0])
    while not rospy.is_shutdown():

        ret,frame = cap.read()

        # warps
        result = perspective_warp(frame)
        # result = region_of_interest(result)
        smallimg=cv2.resize(result, dsize=(64, 48))

        hsl=cv2.cvtColor(result, cv2.COLOR_BGR2HLS)
        imgH,imgS,imgL=cv2.split(hsl)

        imgG=cv2.cvtColor(hsl, cv2.COLOR_BGR2GRAY)

        ret, thr=cv2.threshold(imgG, 127, 255, cv2.THRESH_OTSU)
        
        imgBig = cv2.GaussianBlur(thr, (3,3),0)
        imgBig = region_of_interest(imgBig)

        hist=imgBig.sum(axis=0)
        plt.plot(hist)

        current = np.argmax(hist[:320]), (np.argmax(hist[320:])+320)
        #print(current)

        out_img, angle_degree, center=warp_process_image(imgBig, current)
        queue.popleft()
        queue.append(angle_degree)
        angle_degree=sum(queue)/3
        if angle_degree > 25:
            angle_degree = 25
        elif angle_degree < -25:
            angle_degree = -25
        angle_degree = angle_degree
        result = weighted_img(out_img,result)
        data.data=[int(speed),int(angle_degree),0]

        global mode
        if mode==0:
            pub.publish(data)
 
        cv2.imshow('processing', imgBig)
        cv2.imshow('result', result)
        cv2.imshow('a',frame)
        print(angle_degree)
        # 'q' 키를 누르면 종료합니다.
        if cv2.waitKey(30) == ord('q'):
            break
    # Release the camera and destroy the window
    cv2.destroyAllWindows()



if __name__ == '__main__':
    # 노드초기화
    # 시리얼 포트와 전송할 데이터를 설정합니다.
    rospy.init_node('image_subscriber', anonymous=True)
    speed = 5
    path = '/home/kai/catkin_ws/src/line/scripts/videos/rainrainhigh.avi'
    cap = cv2.VideoCapture(path)
    # 시리얼 포트와 전송할 데이터를 설정합니다.
    pub = rospy.Publisher('SpeedAngleGear', Int8MultiArray, queue_size=10)
    sub=rospy.Subscriber('/gps_mode',Int8,mode_callback)
    rate = rospy.Rate(10) # 10hz
    data = Int8MultiArray()

    main()