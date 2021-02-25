import DatabaseConnection

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
# DatabaseConnection.delete_profile({"welcome":"BCM96318 Broadband Router"})
y = DatabaseConnection.find_profiles_on_device("BCM96318 Broadband Router")
print(y)
