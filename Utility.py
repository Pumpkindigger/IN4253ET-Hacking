import DatabaseConnection

# Test class for DatabaseConnection

example_json = {
  "options": [],
  "welcome": "Broadband Router",
  "login": "Login:",
  "Authentication": "Always",
  "Command Interaction": {
    "command1": "response1",
    "command2": "response2",
    "command3": "response3"
  }
}

# Add example to DB
DatabaseConnection.add_profile(example_json)

# Update command
y = DatabaseConnection.find_profile({"welcome":"Broadband Router"})
print(y)