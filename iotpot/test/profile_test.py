import unittest
from Profiles.ProfileLogic import ProfileLogic
from database_connection import DatabaseConnection

profile1 = {
    "Options": [],
    "Welcome": "BCM96318 Broadband Router\nLogin: ",
    "Authentication": "Always",
    "Command Interaction": {
        "command1": "response1",
        "command2": "response2",
        "command3": "response3"
    }
}


class ProfileTest(unittest.TestCase):
    def setUp(self):
        self.dbcon = DatabaseConnection("test", "profiles")
        self.pl = ProfileLogic(self.dbcon)

    def tearDown(self):
        self.dbcon.mycol.delete_many({})

    def test_insert_profile(self):
        count = self.dbcon.mycol.estimated_document_count()
        self.pl.insert_profile(profile1["Options"], profile1["Welcome"], profile1["Authentication"])
        self.assertEqual(count+1, self.dbcon.mycol.estimated_document_count())

    def test_get_profile(self):
        self.dbcon.add_entry(profile1)
        profile_test_1 = self.pl.get_profile(profile1["Options"], profile1["Welcome"],
                                      profile1["Authentication"])
        self.assertEqual(profile_test_1, profile1["_id"])

        profile_test_2 = self.pl.get_profile(profile1["Options"], profile1["Welcome"] + "welcome",
                                      profile1["Authentication"])
        self.assertEqual(profile_test_2, None)


if __name__ == '__main__':
    unittest.main()
