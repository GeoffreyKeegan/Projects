import unittest
import json
import requests


user_url = 'https://dattafish-user-service.azurewebsites.net/api/user/'
func_key = 'LVCoAgNAc-rTT87yyDtTfawf9BCC_8Kort7nAVYi5XETAzFuudKeRg=='


class TestUserMethods(unittest.TestCase):

    def test_AUTH_user(self):

        print('testing updated GET')


        # User blah tested
        res = requests.post(user_url, params = {"code" : func_key}, json={'username':'blah', 'password':'000'})



        # Test GET by username and password (Successful)
        res = requests.get(user_url, params = {"code" : func_key, 'username':'blah', 'password':'000'})

        self.assertEqual(200, res.status_code)
        print(res.status_code, res.text)




        # Test GET by username and password (Wrong Password)
        res = requests.get(user_url, params = {"code" : func_key, 'username':'blah', 'password':'111'})

        self.assertEqual(404, res.status_code)
        print(res.status_code, res.text)




        # Test GET by username and password (Wrong username)
        res = requests.get(user_url, params = {"code" : func_key, 'username':'bl h', 'password':'111'})

        self.assertEqual(404, res.status_code)
        print(res.status_code, res.text)




        # Test GET by username and password (No username param) - Return all user listing
        res = requests.get(user_url, params = {"code" : func_key, 'password':'111'})

        self.assertEqual(200, res.status_code)
        #print(res.status_code, res.text)




        # Test GET by username and password (No password param) - Return all user listing
        res = requests.get(user_url, params = {"code" : func_key, 'username':'blah'})

        self.assertEqual(200, res.status_code)
        #print(res.status_code, res.text)




        # Test GET by username and password (No user params) - Return all user listing
        res = requests.get(user_url, params = {"code" : func_key})

        self.assertEqual(200, res.status_code)
        #print(res.status_code, res.text)



        # Test GET after DELETE
        res = requests.get(user_url, params = {"code" : func_key, 'username':'blah', 'password':'000'})
        u = json.loads(res.text)
        _id = u.get('_id').get('$oid')

        res = requests.delete(user_url+_id, params = {"code" : func_key})
        self.assertEqual(200, res.status_code)

        res = requests.get(user_url, params = {"code" : func_key, 'username':'blah', 'password':'000'})
        self.assertEqual(404, res.status_code)
        print(res.status_code, res.text)








if __name__ == '__main__':
    unittest.main()