import time
import re
import cv2
import mss
import numpy
import pytesseract
from playsound import playsound

# top left 2224, 160
# top right  2360, 160
# bottom left 2224, 909
# bottom right 2360, 909

# chat top left 440, 1139
# chat top right 600, 1139
# chat bottom left 440, 1363
# chat bottom right 600, 1363

top_right_names = {'top': 168, 'left': 2224, 'width': 132, 'height': 749}
bot_left_names = {'top': 1139, 'left': 440, 'width': 160, 'height': 230}

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

with mss.mss() as sct:
    while True:
        kernel = numpy.ones((1, 1), numpy.uint8)
        
        top_right_image = numpy.asarray(sct.grab(top_right_names))
        top_right_image = cv2.resize(top_right_image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        top_right_image = cv2.cvtColor(top_right_image, cv2.COLOR_BGR2GRAY)
        top_right_image = numpy.invert(top_right_image)
        top_right_image = cv2.dilate(top_right_image, kernel, iterations=1)
        top_right_image = cv2.erode(top_right_image, kernel, iterations=1)

        bot_left_image = numpy.asarray(sct.grab(bot_left_names))
        bot_left_image = cv2.resize(bot_left_image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        bot_left_image = cv2.cvtColor(bot_left_image, cv2.COLOR_BGR2GRAY)
        bot_left_image = numpy.invert(bot_left_image)
        bot_left_image = cv2.dilate(bot_left_image, kernel, iterations=1)
        bot_left_image = cv2.erode(bot_left_image, kernel, iterations=1)

        top_right_text = pytesseract.image_to_string(top_right_image)
        bot_left_text = pytesseract.image_to_string(bot_left_image)

        #cv2.imshow('Image', top_right_image)
        #cv2.imshow('Image', bot_left_image)

        All_Data = top_right_text.splitlines()
        Name_Data = bot_left_text.splitlines()

        all_list = []    
        name_list = []

        for word in All_Data:
            match = re.findall('^[a-zA-Z]+', word)
            if match:
                all_list.append(word)

        for word in Name_Data:
            match = re.findall('^[a-zA-Z]+', word)
            whitelist = word != 'Panic Ahhhh'
            if match and whitelist:
                name_list.append(word)

        print(all_list)
        print(name_list)

        for name in name_list:
            for all_names in all_list:
                if name != '' and name == all_names:
                    playsound('beep.mp3')
        
        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        # One screenshot per second
        time.sleep(1)


