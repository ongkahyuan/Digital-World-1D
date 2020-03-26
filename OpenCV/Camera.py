import numpy as numpy
import cv2

class room_brightness:
    def check_brightness():
        camera_index = 0 # Video camera number 0
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW) #cap as an object, Setting resolution using cap_dshow
        ret, img = cap.read()
        img_dot = img
        lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        y,x,z = img.shape #height, width of image
#         print('>> Image Dimension => X:{}, Y:{}'.format(x,y))
        l_blur = cv2.GaussianBlur(l, (11, 11), 5)
        maxval = []
        count_percent = 10 #percent of total image
        count_percent = count_percent/100
        row_percent = int(count_percent*x) #1% of total pixels widthwise
        column_percent = int(count_percent*y) #1% of total pizel height wise
        for i in range(1,x-1):
            if i%row_percent == 0:
                for j in range(1, y-1):
                    if j%column_percent == 0:
                        pix_cord = (i,j)
                        cv2.circle(img_dot, (int(i), int(j)), 5, (0, 255, 0), 2)
                        img_segment = l_blur[i:i+3, j:j+3]
                        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(img_segment)
                        maxval.append(maxVal)
        avg_maxval = round(sum(maxval) / len(maxval))
#         print('>> Total points: {}'.format(len(maxval)))
#         print('>> Average Brightness: {}'.format(avg_maxval))
        return avg_maxval

#-----------------Get brightness value------------------
# b=room_brightness 
#-----------------Print brightness Value-----------------
# print(b.check_brightness()) 

def Check_light_state():
    b= room_brightness
    if b.check_brightness() >= 50:
        a = True
        # return "Lights in the Room are 'ON'"
    elif b.check_brightness() < 50:
        a = False
        # return "Lights in the Room are 'OFF'"
    return a
         
print(Check_light_state())