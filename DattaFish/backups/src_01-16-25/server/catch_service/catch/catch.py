from bson import ObjectId
import pymongo

mycol = None

### Initialization and reset

def connect(conn_str: str):
    """connect to the client and initialize mycol.  returns none."""
    global mycol
    myclient = pymongo.MongoClient(conn_str)
    mydb = myclient["mydatabase"]
    mycol = mydb["catches"]


def reset():
    """reset the collection.  returns none."""
    mycol.drop()



### CRUD operations
def create_catch(species: str, weight: float, location: str, lure: str, time: str) -> str:
    """returns id of new user"""
    global mycol
    userdict = {"species": species, "weight": weight, "location": location, "lure": lure, "time": time}
    x = mycol.insert_one(userdict)
    return str(x.inserted_id)


def read_catch(id: str) -> dict:
    """returns user document"""
    global mycol
    oid = ObjectId(id)
    myquery = {"_id": oid}
    return mycol.find_one(myquery)


def update_catch(id:str, update):
    """returns modified_count."""
    global mycol
    oid = ObjectId(id)
    result = mycol.update_one({'_id':oid},{'$set':update})
    return result.modified_count


def delete_catch(id:str):
    """returns delete result"""
    oid = ObjectId(id)
    myquery = {'_id': oid}
    mycol.delete_one(myquery)
    return mycol.find_one(myquery)


### Data Tracking
def data_track(cids, q1, q2):
    """returns organized data"""
    global mycol

    data_arr = []
    data_dict = {}


    # q1 is weight
    if q1 == "weight":
        for cid in cids:
            # Read catch
            oid = ObjectId(cid)
            myquery = {"_id": oid}
            catch = mycol.find_one(myquery)
            
            if catch.get(q2[0]) == q2[1]:
                catch_data = (catch.get(q1), cid)
                data_arr.append(catch_data)

        return sorted(data_arr, key=lambda x: x[0], reverse=True)


    # q1 is species, location, lure
    else:
        for cid in cids:
            # Read catch
            oid = ObjectId(cid)
            myquery = {"_id": oid}
            catch = mycol.find_one(myquery)

            if catch.get(q2[0]) == q2[1]:
                d = data_dict.get(catch.get(q1), None)
                if d is None:
                    data_dict[catch.get(q1)] = []
                cid_arr = data_dict.get(catch.get(q1))
                cid_arr.append(cid)

                data_dict.update({catch.get(q1):cid_arr})
            
        keys = data_dict.keys()
        for k in keys:
            catch_data = (data_dict.get(k), k)
            data_arr.append(catch_data)
        return sorted(data_arr, key=lambda x: len(x[0]), reverse=True)