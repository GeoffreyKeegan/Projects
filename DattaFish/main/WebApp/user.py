from flask_login import UserMixin
import json
import requests

user_url = 'https://dattafish-user-service.azurewebsites.net/api/user/'
func_key = 'LVCoAgNAc-rTT87yyDtTfawf9BCC_8Kort7nAVYi5XETAzFuudKeRg=='

class User(UserMixin):
   
    def __init__(self,user_id,username):
        self.id = user_id
        self.username = username
        #self.admin = admin

    def get(user_id):

        ## TODO: Make a request to your user-service to GET user by id
        res = requests.get(user_url+user_id, 
                           params={'code':func_key})

        if res.status_code != 200:
            return None
        
        u = json.loads(res.text)
        user_id = u.get('_id').get('$oid')
        un = u.get('username')
        user = User(user_id, un)
        return user
    

    def authenticate(username, password):

        ## TODO: user-service GET user by username and password
        res = requests.get(user_url, params={'code':func_key, 'username': username, 'password': password})

        if res.status_code != 200:
            return None

        u = json.loads(res.text)
        user_id = u.get('_id').get('$oid')
        un = u.get('username')
        user = User(user_id, un)
        return user
