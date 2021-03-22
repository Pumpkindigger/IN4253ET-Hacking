from Profiles.ProfileLogic import ProfileLogic
from Profiles.DatabaseConnection import DatabaseConnection

file = open('banners.txt', 'r')
lines = file.readlines()
pl = ProfileLogic(DatabaseConnection("myFirstDatabase", "profiles"))

for line in lines:
    line = line.strip()[1:-1]
    pl.insert_profile({}, line, 'Always')