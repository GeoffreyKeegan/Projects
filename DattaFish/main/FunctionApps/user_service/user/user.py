from bson import ObjectId
import pymongo

mycol = None

### Initialization and reset

def connect(conn_str: str):
    """connect to the client and initialize mycol.  returns none."""
    global mycol
    myclient = pymongo.MongoClient(conn_str)
    mydb = myclient["mydatabase"]
    mycol = mydb["users"]


def reset():
    """reset the collection.  returns none."""
    mycol.drop()



### CRUD operations

def create_user(username: str, password: str) -> str:
    """returns id of new user"""
    global mycol
    userdict = {"username": username, "password": password, "catches": []}
    x = mycol.insert_one(userdict)
    return str(x.inserted_id)


def read_user(id: str) -> dict:
    """returns user document"""
    global mycol
    oid = ObjectId(id)
    myquery = {"_id": oid}
    return mycol.find_one(myquery)


def read_users(query: dict) -> list:
    """returns a cursor of user documents matching the query"""
    ret = []
    for d in mycol.find(query):                 
        ret.append(d)
    return ret


def update_user(id:str, update):
    """returns modified_count."""
    global mycol
    oid = ObjectId(id)
    result = mycol.update_one({'_id':oid},{'$set':update})
    return result.modified_count


def update_user_pass(id: str, newpass):
    """returns update result."""
    global mycol
    myquery_new = {'password' : newpass}
    oid = ObjectId(id)
    
    mycol.update_one({'_id': oid}, {'$set': myquery_new})

    return mycol.find_one({'_id': oid})


def delete_user(id:str):
    """returns delete result"""
    oid = ObjectId(id)
    myquery = {'_id': oid}
    mycol.delete_one(myquery)
    return mycol.find_one(myquery)


# Catch Functions
def add_catch (uid:str, cid:str):
    """returns add result"""
    oid = ObjectId(uid)
    myquery = {'_id': oid}
    user = mycol.find_one(myquery)
    catches = user.get('catches')
    catches.insert(0, cid)
    newquery = {"catches" : catches}
    mycol.update_one(myquery, {'$set': newquery})
    return mycol.find_one(myquery)
    
    
def delete_catch (uid:str, cid:str):
    """returns add result"""
    oid = ObjectId(uid)
    myquery = {'_id': oid}
    user = mycol.find_one(myquery)
    catches = user.get("catches")
    catches.remove(cid)
    newquery = {"catches" : catches}
    mycol.update_one(myquery, {'$set': newquery})
    return mycol.find_one(myquery)
    

