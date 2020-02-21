from libdw import pyrebase

class pyrebase_IO():
    """Class to create, modify, and access entries in database"""

    def __init__(self):
        """Initializes connection to firebase"""

        projectid = "fir-is-pleb"
        dburl = "https://" + projectid + ".firebaseio.com"
        authdomain = projectid + ".firebaseapp.com"
        apikey = "AIzaSyDInE2UqPevyizfRYUVD80GePYJozsYToQ"
        email = "joel2_ong@mymail.sutd.edu.sg"
        password = "password"

        config = {
            "apiKey": apikey,
            "authDomain": authdomain,
            "databaseURL": dburl,
        }

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        self.user = auth.sign_in_with_email_and_password(email, password)
        self.db = firebase.database()

    def write_node(self, key, value, child1 = None, child2 = None):
        """Writes to node, both for updates and creation.
        Arguments:
            - key: key for the pair
            - value: value for the pair
        Optional Arguments:
            - child1: Node name, sublevel 1
            - child2: Node name, sublevel 2""" 

        if child1 == None and child2 == None:
            self.db.child(str(key)).set(value,self.user['idToken'])
        elif child2 == None:
            self.db.child(str(key)).child(str(child1)).set(value,self.user['idToken'])
        else:
            self.db.child(str(key)).child(str(child1)).child(str(child2)).set(value,self.user['idToken'])

    def read_node(self, key, child1 = None, child2 = None):
        """Reads node, returns value / object in database
        Arguments:
            - key: key for the pair
        Optional Arguments:
            - child1: Node name, sublevel 1
            - child2: Node name, sublevel 2""" 
    
        if child1 == None and child2 == None:
            return self.db.child(str(key)).get(self.user['idToken']).val()
        elif child2 == None:
            return self.db.child(str(key)).child(str(child1)).get(self.user['idToken']).val()
        else:
            return self.db.child(str(key)).child(str(child1)).child(str(child2)).get(self.user['idToken']).val()