import unittest
import json
import requests


# catch_url = None
# func_key = None

points = 0

class TestUserMethods(unittest.TestCase):

    def test_CRUD_user(self):

        global points

        print('testing CRUD operations')

        # Create
        res = requests.post(catch_url,
                            params = {"code" : func_key},
                            json={
                                'species': 'Largemouth Bass',
                                'weight': 3.89,
                                'location': 'Ottarnic',
                                'lure': 'Rage Menace (Black/Blue)',
                                'time': '7/27/23 (7:00pm)'})
        print(res.status_code, res.text)        
        self.assertTrue(res.status_code in [200,201])        
        _id = res.text

        points+=1

        # Update
        res = requests.put(catch_url+_id,
                           params = {"code" : func_key},
                           json={"lure":'senko'})
        print(res.status_code,res.text)
        self.assertEqual(res.status_code,200)

        points+=1


        # Read
        res = requests.get(catch_url+_id,
                           params = {"code" : func_key})
        print(res.status_code, res.text)
        u = json.loads(res.text)
        self.assertEqual(u.get('lure'),'senko')
        _id = u.get('_id').get('$oid')

        points+=1


        # Delete
        res = requests.delete(catch_url+_id,
                              params = {"code" : func_key})
        print(res.status_code, res.text)
        self.assertEqual(res.status_code,200)

        points+=1

        res = requests.get(catch_url+_id,
                           params = {"code" : func_key})
        self.assertEqual(res.status_code,404)

        points+=1


        # Data Tracker
        id_arr = []
        res = requests.post(catch_url,
                            params = {"code" : func_key},
                            json={
                                'species': 'Largemouth Bass',
                                'weight': 3.01,
                                'location': 'Ottarnic',
                                'lure': 'Senko (Black/Blue)',
                                'time': '7/27/23 (7:00pm)'})
        id_arr.append(res.text)

        res = requests.post(catch_url,
                            params = {"code" : func_key},
                            json={
                                'species': 'Largemouth Bass',
                                'weight': 1.4,
                                'location': 'Darrah',
                                'lure': 'Rage Menace (Green Pumpkin)',
                                'time': '7/27/23 (7:00pm)'})
        id_arr.append(res.text)
        res = requests.post(catch_url,
                            params = {"code" : func_key},
                            json={
                                'species': 'Largemouth Bass',
                                'weight': 3.89,
                                'location': 'Ottarnic',
                                'lure': 'Rage Menace (Black/Blue)',
                                'time': '7/27/23 (7:00pm)'})
        id_arr.append(res.text)
        res = requests.post(catch_url,
                            params = {"code" : func_key},
                            json={
                                'species': 'Chain Pickerel',
                                'weight': 2.33,
                                'location': 'Ottarnic',
                                'lure': 'Rage Menace (Black/Blue)',
                                'time': '7/27/23 (7:00pm)'})
        id_arr.append(res.text)
        res = requests.post(catch_url,
                            params = {"code" : func_key},
                            json={
                                'species': 'Bluegill',
                                'weight': .09,
                                'location': 'Minefalls',
                                'lure': 'Hair Jig (Black/Blue)',
                                'time': '7/27/23 (7:00pm)'})
        id_arr.append(res.text)     

    
        res = requests.post(catch_url+"data",
                           params = {"code" : func_key},
                           json={"cids": id_arr, "q1" :"weight", "q2": ("species", "Largemouth Bass")})
        
        self.assertEqual(res.status_code,200)
        print(res.text)




    def test_print_points(self):

        print('printing points')
        global points
        print(points)


if __name__ == '__main__':
    unittest.main()

