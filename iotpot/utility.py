from database_connection import DatabaseConnection
from profile_logic import ProfileLogic

# Test class for DatabaseConnection

example_json = {
  "Options": [],
  "Welcome": "BCM96318 Broadband Router",
  "Authentication": "Always",
  "Command Interaction": {
    "command1": "response1",
    "command2": "response2",
    "command3": "response3"
  }
}

# Add example to DB
# DatabaseConnection.add_profile(example_json)

# Update command
# DatabaseConnection.delete_profile({"Welcome":"BCM96318 Broadband Router"})
dbcon = DatabaseConnection("myFirstDatabase","profiles")
y = dbcon.get_random_entry()
print(y)

profile_1 = {
  "Options": ["DO(echo)", "DO(rflow)", "WILL(echo)", "WILL(sga)"],
  "Welcome": "BCM96318 Broadband Router",
  "Authentication": "Always",
  "Command Interaction": {
    "command1": "response1",
    "command2": "response2",
    "command3": "response3"
  }
}

pl = ProfileLogic(dbcon)
pl.insert_profile(profile_1["Options"], profile_1["Welcome"], profile_1["Authentication"])
