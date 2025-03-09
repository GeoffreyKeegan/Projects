import unittest
import catch

conn_str = "mongodb://localhost:27017/"

# species: str, weight: float, location: str, lure: str, time: str

class TestCatchMethods(unittest.TestCase):

    def test_CRUD(self):

        catch.connect(conn_str)
        catch.reset()

        uid = catch.create_catch("LMB", 3.90, "Darrah", "Senko (Green Pumpkin)", "08/14/24")
        self.assertIsNotNone(uid)


        uid = catch.create_catch("SMB", 3.05, "Merrimack River", "Rage Menace (Green Pumpkin)", "07/11/24")
        #print(uid)
        u = catch.read_catch(uid)
        print(u)
        self.assertTrue(u.get('species')=='SMB')


        uid = catch.create_catch("LMB", 3.89, "Ottarnic", "Rage Menace (Green Pumpkin)", "07/11/23")
        u = catch.update_catch(uid,{"lure": "Rage Menace (Blue/Black)"})
        #print(u)

        u = catch.read_catch(uid)
        self.assertEqual(u.get('lure'),"Rage Menace (Blue/Black)")


        uid = catch.create_catch("LMB", 3.89, "Ottarnic", "Rage Menace (Green Pumpkin)", "07/11/23")
        result = catch.delete_catch(uid)
        #print(result)
        u = catch.read_catch(uid)
        #print(u)

        self.assertIsNone(u)

if __name__ == '__main__':
    unittest.main()
