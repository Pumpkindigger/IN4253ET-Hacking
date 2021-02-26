from DatabaseConnection import DatabaseConnection
from ProfileLogic import ProfileLogic

# Test class for DatabaseConnection

example_json = {
  "Options": [],
  "Welcome": "BCM96318 Broadband Router",
  "Login": "Login",
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
y = dbcon.find_profiles_on_device("BCM96318 Broadband Router")
print(y)

profile_1 = {
  "Options": ["DO(echo)", "DO(rflow)", "WILL(echo)", "WILL(sga)"],
  "Welcome": "BCM96318 Broadband Router",
  "Login": "Telnet is Disabled in WAN Side",
  "Authentication": "Always",
  "Command Interaction": {
    "command1": "response1",
    "command2": "response2",
    "command3": "response3"
  }
}

pl = ProfileLogic(dbcon)
pl.insert_profile(profile_1["Options"], profile_1["Welcome"], profile_1["Login"], profile_1["Authentication"])
