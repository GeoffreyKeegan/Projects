import unittest
import json
import requests


user_url = None
func_key = None


class TestUserMethods(unittest.TestCase):

    # User CRUD
    def test_CRUD_user(self):

        print('testing CRUD operations')

        # CREATE
        res = requests.post(user_url,
                            params = {"code" : func_key},
                            json={
                                'username':'dave2',
                                'password':'evad'})
        print(res.status_code, res.text)        
        self.assertTrue(res.status_code in [200,201])        
        _id = res.text


        # UPDATE
        res = requests.put(user_url+_id,
                           params = {"code" : func_key},
                           json={"password":'vade'})
        print(res.status_code,res.text)
        self.assertEqual(res.status_code,200)


        # READ
        res = requests.get(user_url+_id,
                           params = {"code" : func_key})
        print(res.status_code, res.text)
        u = json.loads(res.text)
        self.assertEqual(u.get('password'),'vade')
        _id = u.get('_id').get('$oid')


        # DELETE
        res = requests.delete(user_url+_id,
                              params = {"code" : func_key})
        print(res.status_code, res.text)
        self.assertEqual(res.status_code,200)
        res = requests.get(user_url+_id,
                           params = {"code" : func_key})
        self.assertEqual(res.status_code,404)



    # Add and Delete Catch
    
    def test_Add_Delete_catch(self):

        print('testing Add Delete catch operations')

        res = requests.post(user_url,
                            params = {"code" : func_key},
                            json={
                                'username':'dave',
                                'password':'evad'})             
        _id = res.text


        # ADD Catch
        res = requests.post(user_url+_id+"/catches",
                            params = {"code" : func_key},
                            json={
                                'uid':_id,
                                'cid':'123'})
        self.assertTrue(res.status_code in [200,201]) 

        print(res.status_code, res.text)


        # DELETE Catch
        res = requests.delete(user_url+_id+"/catches",
                            params = {"code" : func_key},
                            json={
                                'uid':_id,
                                'cid':'123'})
        self.assertTrue(res.status_code in [200,201]) 

        print(res.status_code, res.text)
        


if __name__ == '__main__':
    unittest.main()

