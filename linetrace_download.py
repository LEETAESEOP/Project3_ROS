import cv2
import requests
import numpy as np
import math

#이미지 사이즈 320x240
#크롭 영역(라인 추적 영역)
image_crop_x1 = 0
image_crop_y1 = 100
image_crop_x2 = 319
image_crop_y2 = 239

URL = "http://192.168.31.69" #사진가져오기 URL 주소

minLineLength = 5
maxLineGap = 10

while True:
    image_nparray = np.asarray(bytearray(requests.get(URL+"/picture").content), dtype=np.uint8)
    image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
    image = cv2.flip(image,0)
    image = cv2.flip(image,1)
    original = image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cropped = gray[image_crop_y1:image_crop_y2,image_crop_x1:image_crop_x2]
#    blurred = cv2.GaussianBlur(cropped, (5, 5), 0)
    blurred = cropped
    edged = cv2.Canny(blurred, 85, 85)
    lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
    max_diff = 1000
    final_x = 0
    if ( lines is not None ):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(original,(x1+image_crop_x1,y1+image_crop_y1),(x2+image_crop_x1,y2+image_crop_y1),(0,255,0),2)
            mid_point = ( x1 + x2 ) / 2
            diff = abs((320/2) - mid_point)
            if ( max_diff > diff ) :
                max_diff = diff
                final_x = mid_point
    
    if ( int(final_x) != 0 ) :
        original = cv2.circle(original,(int(final_x),int((image_crop_y1+image_crop_y2)/2)),5,(0,0,255),-1)
        original = cv2.rectangle(original,(int(image_crop_x1),int(image_crop_y1)),(int(image_crop_x2),int(image_crop_y2)),(0,0,255),1)
    image = original
    cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("result", image)
    if cv2.waitKey(1) & 0xFF == ord('q'): break
    theta = int(( int(final_x) - 160.0 ) / 320.0 * 100)
    response = requests.get(url = URL + "/dir", params={"value": str(theta)})
    print(theta)
