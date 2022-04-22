#예제 2.7은 웹캡 캡쳐부분이라 뺐음. 2.8에서 cv2.VideoCapture(0)만 넣어주면됨
#예제2.8 ''비디오 입력과 화면표시 2: 안드로이드 스마트폰 p31
# ddepth 가 뭔가?

import cv2
import os
import numpy as np
import time
os.system('cls')

# 이미지 사이즈 320x240
# #크롭 영역(라인 추적 영역)
# image_crop_x1 = 0
# image_crop_y1 = 100
# image_crop_x2 = 319
# image_crop_y2 = 239

# 이미지 사이즈 640 * 480
#크롭 영역(라인 추적 영역)
frame_crop_x1 = 0
frame_crop_y1 = 200
frame_crop_x2 = 639
frame_crop_y2 = 479

minLineLength = 40
maxLineGap = 20

#droid cam
cap = cv2.VideoCapture(0)  #노트북은 0 데스크탑은 1

# 원본 동영상 크기 정보
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("원본 동영상 너비(가로) : {}, 높이(세로) : {}".format(w, h))

# 동영상 크기 변환 원할시 아래 주석 풀고 숫자만 바꿔주면 된다.
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320) # 가로
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) # 세로


while True:
    retval, frame = cap.read()
    # 카메라를 뒤집어 쓸지 그대로 쓸지 선택하는곳
    # frame = cv2.flip(frame,1)
    # frame = cv2.flip(frame,0)
    # frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY)
    original = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(cropped, (5, 5), 0)
    blurred = gray[frame_crop_y1:frame_crop_y2,frame_crop_x1:frame_crop_x2]

    # 아래 두줄 추가한 부분
    # 영상을 부드럽게 하는 블러필터 중 boxFilter를 사용하여 영상의 잡음을 제거하고 영상을 부드럽게 한다.
    # ddepth = -1 이면 blurred 와 같은 깊이다. ksize가 클수록 화면이 더 부드러워진다.  
    blurred = cv2.boxFilter(blurred, ddepth=-1, ksize=(31,31))
    # cv2.threshold(img, threshold_value, value, flag) 형식이다.
    # threshold는 임계값 영상을 출력한다. THRESH_BINARY를 사용하면 2개의 값만 갖는다.(흑,백)
    # 아래에서 100=임계점이며, 0~100 의 값들은 255로 표현된다. 255=완전 백색을 의미한다.
    retval2 ,blurred = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)
    cv2.imshow('blurred', blurred)

    
    
    # cv2.Canny(gray_img, threshold1, threshold2) 형식이다.
    # cv2.Canny() 는 엣지 검출 함수다. 이미지의 엣지만을 리턴한다.
    # threshold1 = 낮은 경계값(0~255), threshold2 = 높은 경계값(0~255)
    # threshold1, threshold2 값의 숫자가 클수록 엣지가 검출되기 어렵다.
    edged = cv2.Canny(blurred, 85, 85)
    cv2.imshow('edged', edged)
    # 허프(Hough) 변환. 이미지의 Line을 찾는것이 목적이다.
    # HoughLinesP 설명     (img, rho, theta, threshold, lines, minLineLength, maxLineGap)
    # img : 8bit, single-channel binary image, canny edge를 선 적용.
    # rho : r 값의 범위 (0 ~ 1 실수),        theta: 각도, 라디안 단위 (np.pi/0~180)
    # threshold: 직선으로 판단할 최소한의 동일 개수(점의 개수) (작은 값: 정확도 감소, 검출 개수 증가 / 큰 값: 정확도 증가, 검출 개수 감소)
    # minLineLength : 선으로 인정할 최소 길이. 이 값보다 작으면 reject.
    # maxLineGap = 직선 위의 에지들의 최대 허용간격. 이 값보다 작으면 reject. (에지가 중간에 끊겼을때 1로하면 조금만 끊겨도 선을 끊어버림.)
    lines = cv2.HoughLinesP(edged, 1, np.pi/180, 10, minLineLength, maxLineGap)
    #lines : 10개일경우 아래처럼 데이타 출력된다.
    #     S좌표    F좌표
    #  [ x1   y1 / x2  y2 ]
    # [[[151 182 165 160]]
    # [[467 104 471 114]]      
    # [[136 205 146 189]]      
    # [[203 100 224  64]]      
    # [[514 231 519 246]]      
    # [[454  74 458  84]]
    # [[501 192 504 202]]
    # [[166 159 176 143]]
    # [[ 99 264 118 235]]
    # [[484 145 489 159]]]


    max_diff = 1000
    final_x = 0

    # 라인이 검출될 때
    if ( lines is not None ):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # print("x1, y1, x2, y2", line[0])
            # 녹색 선 그리기
            # 이미지 파일, 시작점 좌표, 종료점 좌표, 선색상, 선두께) 
            cv2.line(original,(x1+frame_crop_x1,y1+frame_crop_y1),(x2+frame_crop_x1,y2+frame_crop_y1),(0,255,0),3)
            # 녹색선의 x위치 중간값
            mid_point = ( x1 + x2 ) / 2
            # 화면 중앙 x값과, 녹색선의 중앙x값의 차이값을 구한다.
            diff = abs((640/2) - mid_point)
            # print("mid_point, diff", mid_point, diff)
            if ( max_diff > diff ) :
                max_diff = diff
                # final_x : 녹색선 중앙의 x 좌표점이 된다.
                final_x = mid_point
    
    if ( int(final_x) != 0 ) :
        # 빨간점 인식 포인트, 이때 녹색선의 x값 중앙점을 가르킴. y좌표는 화면 중앙. 원 두께는 5
        original = cv2.circle(original,(int(final_x),int((frame_crop_y1+frame_crop_y2)/2)),5,(0,0,255),-1)
        # 빨간 사각 영역
        original = cv2.rectangle(original,(int(frame_crop_x1),int(frame_crop_y1)),(int(frame_crop_x2),int(frame_crop_y2)),(0,0,255),1)
    frame = original
    
    # 카메라 입력값 없으면 break
    if not retval:
        break
    # 최종 화면
    cv2.imshow('frame', frame)
    theta = int(( int(final_x) - 320.0 ) / 640.0 * 100)
    print("theta: ", theta)
    
    key = cv2.waitKey(25)
     # ESC 입력시 종료
    if key == 27: #ESC 아스키코드값이 27
        break

if cap.isOpened():
    cap.release()

cv2.destroyAllWindows()