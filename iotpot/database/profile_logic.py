'''
    Insert, update and get profiles to/from database
    An example profile:
    {
        "Options": []],
        "Welcome": "BCM96318 Broadband Router\n please login",
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

    def insert_profile(self, options, welcome, authentication):
        '''
        Insert a new profile if there is no profile with these options, welcom message, login message and authentication mode
        The new profile will have an empty command interaction field
        '''
        if self.get_profile(options, welcome, authentication) is None:
            profile = {
                "Options": options,
                "Welcome": welcome,
                "Authentication": authentication,
                "Command Interaction": {}
            }
            self.dbcon.add_entry(profile)

    def update_commands(self, profile, command, response):
        '''
        Add to a certain profile a new command and the response (also a command)
        '''
        commands = profile["Command Interaction"]
        commands[command] = response
        query = {"_id": profile["_id"]}
        new_value = {"$set": {"Command Interaction": commands}}
        self.dbcon.update_entry(query, new_value)

    def get_profiles_from_device_name(self, device):
        '''
        Given the welcome message, return a list of profiles
        '''
        profiles = []
        for profile in self.dbcon.find_entries({"Welcome": device}):
            profiles.append(profile)
        return profiles

    def get_profile(self, options, welcome, authentication):
        '''
        Retrieve the id of a profile from the database given the options, welcome message, login message and authentication mode
        '''
        profile = self.dbcon.find_entry({'$and': [{"Options": options}, {"Welcome": welcome},
                                                  {"Authentication": authentication}]})
        if profile is None:
            return None
        else:
            return profile["_id"]

    def get_random_profile(self):
        return self.dbcon.get_random_entry()
