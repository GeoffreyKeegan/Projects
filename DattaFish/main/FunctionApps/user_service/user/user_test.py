import unittest
import user

conn_str = None

class TestUserMethods(unittest.TestCase):

    def test_CRUD(self):
       
        user.connect(conn_str)
        user.reset()


        # Create
        uid = user.create_user("John","Johnspassword")
        self.assertIsNotNone(uid)
            #self.assertEqual(uid.count_documents({}),0)


        # Read One
        uid = user.create_user("John","Johnspassword")
            #print(uid)
        u = user.read_user(uid)
            #print(u)
        self.assertTrue(u.get('username')=='John')


        # Read All
        user.create_user("Jane","Janespass")
        user.create_user("John","password")
        user.create_user("John2","password")    
        us = user.read_users({'password':'password'})
            #print(list(us))
        self.assertEqual(len(list(us)),2)


        # Update Password
        uid = user.create_user("Jane","Janespass")
        u = user.update_user_pass(uid,"Janesnewpass")
            #print(u)
        u = user.read_user(uid)
        self.assertEqual(u.get('password'),"Janesnewpass")


        # Delete
        result = user.delete_user(uid)
            #print(result)
        u = user.read_user(uid)
            #print(u)
        self.assertIsNone(u)


        # Add catch
        uid = user.create_user("Jane","Janespass")
        result = user.add_catch(uid, "123")
            #print(result)
        u = user.read_user(uid)
        self.assertEqual(u.get('catches'),["123"])


        # Delete catch
        result = user.delete_catch(uid, "123")
            #print(result)
        u = user.read_user(uid)
        self.assertEqual(u.get('catches'),[])
        user.delete_user(uid)




if __name__ == '__main__':
    unittest.main()
