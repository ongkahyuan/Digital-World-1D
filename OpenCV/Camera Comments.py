import numpy as numpy
import cv2

class room_brightness: # Creating class
    def check_brightness(): #Creating function within class
        #------------------------Reading image--------------------------------------
        camera_index = 0 # Video camera number 0
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW) #cap as an object, Setting resolution using cap_dshow
        ret, img = cap.read() #returning image as reading cap Object
        #------------------------ My Test Image-------------------------------------
        # img = cv2.imread('CC.png')

        img_dot = img
        #-----Converting image to LAB Color model----------------------------------- 
        lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

        #-----Splitting the LAB image to different channels-------------------------
        l, a, b = cv2.split(lab)

        #-----Finding average lightness level in image by fixing some points--------
        y,x,z = img.shape #height, width of image
        # print('>> Image Dimension => X:{}, Y:{}'.format(x,y))                             # Prints the resolution of image
        #Deciding some dynamic points on image for checking light intensity
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
        # print('>> Total points: {}'.format(len(maxval)))                                  # Prints total points of data taken from image
        # print('>> Average Brightness: {}'.format(avg_maxval))                             # Prints average brightness of points of data taken
        return avg_maxval # Returns the brightness level
        cv2.namedWindow('img', cv2.WINDOW_AUTOSIZE) #This and below shows the picture taken
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
b=room_brightness
print(b.check_brightness())

def Check_light_state():
    b= room_brightness
    if b.check_brightness() >= 50:
        a = True
        return "Lights in the Room are 'ON'"
    elif b.check_brightness() < 50:
        a = False
        return "Lights in the Room are 'OFF'"
         
print(Check_light_state())