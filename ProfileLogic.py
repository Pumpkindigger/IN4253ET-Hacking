import DatabaseConnection

'''
    Insert, update and get profiles to/from database
    An example profile:
    {
        "Options": []],
        "Welcome": "BCM96318 Broadband Router",
        "Login": "Login",
        "Authentication": "Always",
        "Command Interaction": {
          "command1": "response1",
          "command2": "response2"
        }
    }
'''


class ProfileLogic:
    def __init__(self, dbcon):
        self.dbcon = dbcon

    def insert_profile(self, options, welcome, login, authentication):
        '''
        Insert a new profile if there is no profile with these options, welcom message, login message and authentication mode
        The new profile will have an empty command interaction field
        '''
        if self.get_profile(options, welcome, login, authentication) is None:
            profile = {
                "Options": options,
                "Welcome": welcome,
                "Login": login,
                "Authentication": authentication,
                "Command Interaction": {}
            }
            self.dbcon.add_profile(profile)

    def update_commands(self, profile, command, response):
        '''
        Add to a certain profile a new command and the response (also a command)
        '''
        commands = profile["Command Interaction"]
        commands[command] = response
        query = {"_id": profile["_id"]}
        new_value = {"$set": {"Command Interaction": commands}}
        self.dbcon.update_profile(query, new_value)

    def get_profile(self, options, welcome, login, authentication):
        '''
        Retrieve the id of a profile from the database given the options, welcome message, login message and authentication mode
        '''
        profile = self.dbcon.find_profile({'$and': [{"Options": options}, {"Welcome": welcome}, {"Login": login},
                                                    {"Authentication": authentication}]})
        if profile is None:
            return None
        else:
            return profile["_id"]