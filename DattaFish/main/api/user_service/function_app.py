import azure.functions as func
import logging
from bson import json_util
from user import user


conn_str = None
user.connect(conn_str)
app = func.FunctionApp()



#######------USER_CRUD------#######

####------POST------####
@app.route(route="user", methods=['POST'], auth_level=func.AuthLevel.FUNCTION)
def create_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('creating user.')
   
    req_body = req.get_json()
    username = req_body.get('username')
    password = req_body.get('password')

    if len(user.read_users({"username": username})) != 0:
        return func.HttpResponse("username taken", status_code=401)

    uid = user.create_user(username,password)
    return func.HttpResponse(str(uid), status_code=201)




####------GET------####
@app.route(route="user/{_id?}", methods=['GET'], auth_level=func.AuthLevel.FUNCTION)
def read_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('reading user.')

    _id = req.route_params.get('_id')
    username = req.params.get('username')
    password = req.params.get('password')

    if _id:  # If an ID is provided, fetch that user
        u = user.read_user(_id)
        if u is None:
            return func.HttpResponse("User Not found.", status_code=404)

        return func.HttpResponse(json_util.dumps(u), status_code=200)

    elif username and password:
        us = user.read_users({'username': username, 'password': password})
        us = list(us)

        if us:
            return func.HttpResponse(json_util.dumps(us[0]), status_code=200)
        else:
            return func.HttpResponse("User Not Found", status_code=404)
        
    # If no ID, username, and password provided, return all users
    all_users = user.read_users({})
    return func.HttpResponse(json_util.dumps(all_users), status_code=200)
  



####------PUT------####
@app.route(route="user/{_id?}", methods=['PUT'], auth_level=func.AuthLevel.FUNCTION)
def update_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('updating user.')

    _id = req.route_params.get('_id')
    if not _id: # incorrect parameters error
        return func.HttpResponse(
            "incorrect parameters",
            status_code = 400
        )
    

    update = req.get_json()
    u = user.update_user(_id, update)
    return func.HttpResponse(str(u), status_code=200)




####------DELETE------####
@app.route(route="user/{_id?}", methods=['DELETE'], auth_level=func.AuthLevel.FUNCTION)
def delete_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('deleting user.')

    _id = req.route_params.get('_id')
    if not _id: # incorrect parameters error
        return func.HttpResponse("incorrect parameters", status_code = 400)

    u = user.delete_user(_id)

    # Check the result of the deletion
    if u is not None:
        return func.HttpResponse(
            "User Not found.",
            status_code = 404
        )
    
    return func.HttpResponse(str(u), status_code=200)




#######------CATCHES------#######

####------POST------####
@app.route(route="user/{_id?}/catches", methods=['POST'], auth_level=func.AuthLevel.FUNCTION)
def add_catch(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('adding catch.')
   
    req_body = req.get_json()
    uid = req.route_params.get('_id')
    cid = req_body.get('cid')

    result = user.add_catch(uid,cid)
    return func.HttpResponse(str(result), status_code=201)




####------DELETE------####
@app.route(route="user/{_id?}/catches", methods=['DELETE'], auth_level=func.AuthLevel.FUNCTION)
def delete_catch(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('deleting catch.')
   
    req_body = req.get_json()
    uid = req.route_params.get('_id')
    cid = req_body.get('cid')

    result = user.delete_catch(uid,cid)
    return func.HttpResponse(str(result), status_code=201)
