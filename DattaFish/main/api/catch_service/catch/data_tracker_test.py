import unittest
import catch

conn_str = None

# species: str, weight: float, location: str, lure: str, time: str

class TestCatcDatahMethods(unittest.TestCase):

    def test_data(self):
       
        catch.connect(conn_str)
        catch.reset()

        cids = []

        cids.append(catch.create_catch("LMB", 3.90, "Ottarnic", "Senko (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("LMB", 1.43, "Darrah", "Rage Menace (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("BC", .78, "Mine Falls", "Senko (Junebug)", "08/14/24"))
        cids.append(catch.create_catch("SMB", 2.90, "Merrimack River", "Whopper Plopper 75", "08/14/24"))
        cids.append(catch.create_catch("BG", 1.10, "Darrah", "Rage Menace (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("YP", .45, "Ottarnic", "Lil Blade Jig [ButterWorm]", "08/14/24"))
        cids.append(catch.create_catch("LMB", 2.30, "Ottarnic", "Senko (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("SMB", 1.90, "Merrimack River", "Senko (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("LMB", 2.73, "Darrah", "Senko (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("LMB", 1.82, "Darrah", "Rage Menace (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("SMB", 1.12, "Merrimack River", "Senko (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("BG", .80, "Merrimack River", "Rage Menace (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("CP", 2.27, "Ottarnic", "Jerkbait (Bluegill)", "08/14/24"))
        cids.append(catch.create_catch("SMB", 2.33, "Merrimack River", "Whopper Plopper 75", "08/14/24"))
        cids.append(catch.create_catch("LMB", 1.76, "Darrah", "Senko (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("CP", 1.2, "Ottarnic", "Rage Menace (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("LMB", 3.45, "Mine Falls", "Senko (Junebug)", "08/14/24"))
        cids.append(catch.create_catch("LMB", 3.23, "Mine Falls", "Senko (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("LMB", 1.89, "Darrah", "Senko (Green Pumpkin)", "08/14/24"))
        cids.append(catch.create_catch("BG", 1.02, "Ottarnic", "Lil Spoon (Bluegill)", "08/14/24"))

        data = catch.data_track(cids, "lure", ("species", "BG"))
        # data = catch.data_track(cids, "location", ("species", "LMB"))
        # data = catch.data_track(cids, "location", ("species", "BG"))
        
        print(data)

        

if __name__ == '__main__':
    unittest.main()