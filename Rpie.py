from Firebase import pyrebase_IO

db = pyrebase_IO()

db.write_node("hello there","jedtellme")

print(db.read_node("input").val())
