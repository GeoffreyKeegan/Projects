import azure.functions as func
import logging
from bson import json_util
from catch import catch


conn_str = None
catch.connect(conn_str)
app = func.FunctionApp()


#########------CRUD------#########

####------POST------####
@app.route(route="catch", methods=['POST'], auth_level=func.AuthLevel.FUNCTION)
def create_catch(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('creating catch.')
   
    req_body = req.get_json()
    
    species = req_body.get('species')
    weight = req_body.get('weight')
    location = req_body.get('location')
    lure = req_body.get('lure')
    time = req_body.get('time')

    cid = catch.create_catch(species, weight, location, lure, time)
    return func.HttpResponse(str(cid), status_code=201)






####------GET------####
@app.route(route="catch/{_id?}", methods=['GET'], auth_level=func.AuthLevel.FUNCTION)
def read_catch(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('reading catch.')

    _id = req.route_params.get('_id')

    c = catch.read_catch(_id)
    if c is None:
        return func.HttpResponse("Catch Not found.", status_code=404)

    return func.HttpResponse(json_util.dumps(c), status_code=200)

  



####------PUT------####
@app.route(route="catch/{_id?}", methods=['PUT'], auth_level=func.AuthLevel.FUNCTION)
def update_catch(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('updating catch.')

    _id = req.route_params.get('_id')
    if not _id: # incorrect parameters error
        return func.HttpResponse(
            "incorrect parameters",
            status_code = 400
        )
    

    update = req.get_json()
    c = catch.update_catch(_id, update)
    return func.HttpResponse(str(c), status_code=200)

    




####------DELETE------####
@app.route(route="catch/{_id?}", methods=['DELETE'], auth_level=func.AuthLevel.FUNCTION)
def delete_catch(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('deleting catch.')

    _id = req.route_params.get('_id')
    if not _id: # incorrect parameters error
        return func.HttpResponse("incorrect parameters", status_code = 400)

    c = catch.delete_catch(_id)

    # Check the result of the deletion
    if c is not None:
        return func.HttpResponse(
            "Catch Not found.",
            status_code = 404
        )
    
    return func.HttpResponse(str(c), status_code=200)


    
#########------Data Tracker------#########

####------POST------####
@app.route(route="catch/data", methods=['POST'], auth_level=func.AuthLevel.FUNCTION)
def data_track(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('compiling data.')
    req_body = req.get_json()
    cids = req_body.get('cids')
    q1 = req_body.get('q1')
    q2 = req_body.get('q2')

    if cids and q1 and q2: # incorrect parameters error
        data = catch.data_track(cids, q1, q2)
        return func.HttpResponse(json_util.dumps(data), status_code=200)
    else:
        return func.HttpResponse(
            "incorrect parameters",
            status_code = 400
        )