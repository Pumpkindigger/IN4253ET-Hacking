from Profiles.ProfileLogic import ProfileLogic
from Profiles.DatabaseConnection import DatabaseConnection

file = open('banners.txt', 'r')
bannerList = file.readlines()
pl = ProfileLogic(DatabaseConnection("profileDB", "profiles"))

for banner in bannerList:
    banner = banner.strip()[1:-1]
    pl.insert_profile({}, banner, 'Always')