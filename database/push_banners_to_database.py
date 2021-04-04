from iotpot.database.profile_logic import ProfileLogic
from iotpot.database.database_connection import DatabaseConnection

file = open('banners.txt', 'r')
bannerList = file.readlines()
pl = ProfileLogic(DatabaseConnection("profileDB", "profiles"))

for banner in bannerList:
    banner = banner.strip()[1:-1]
    pl.insert_profile({}, banner, 'Always')
