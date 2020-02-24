from Firebase import pyrebase_IO
from OpenCV import Camera

db = pyrebase_IO()
cvobj = Camera.room_brightness()

# testing the pyrbase module:
db.write_node("hello there","jedtellme")
db.write_node("hello there","jedtellme",child1="General Kenobi!")
# print(db.read_node("input"))
# print(db.read_node("hello there",child1="General Kenobi!"))
print(db.read_node("/"))
