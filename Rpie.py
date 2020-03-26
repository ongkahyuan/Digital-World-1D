from Firebase import pyrebase_IO
from OpenCV import Camera
from YOLO.yolo_cam import yolo_manager 
from Sound import sound_manager
import time

db = pyrebase_IO()
cvobj = Camera.room_brightness()
yolo_obj = yolo_manager()
sound = sound_manager.sound_detector()

def test_firebase():
    # testing the pyrbase module:
    db.write_node("hello there","jedtellme")
    db.write_node("hello there","jedtellme",child1="General Kenobi!")
    # print(db.read_node("input"))
    # print(db.read_node("hello there",child1="General Kenobi!"))
    print(db.read_node("/"))

def test_yolo():
    # testing yolo module
    print(yolo_obj.check_room_state())

def test_sound():
    sound.start()
    # time.sleep(60*5)
    # sound.stop_all()

# test_yolo()
time_start = time.time()
sound.start()
yolo_obj.start()

while time.time()-time_start<60*1: 
    print("Sound: ", end= '')
    sound_types = ["silent", "voice", "music"]
    try:
        print(sound_types[sound.is_sound])
    except:
        print("not enough data")
    print("yolo: ", end='')
    print(yolo_obj.room_state)
    print('\n')
    time.sleep(5)

sound.stop_all()
yolo_obj.stop_all()
print("end")
    