import time
"""
    Insert, update and get logging to/from database
    An example logging:
    {
        "timestamp": 1615974192, # Unix Timestamp
        "profile_id": "6037aa31a3287bce5a2c440c", # Unique ID from profile entry
        "client_ip": "127.0.0.1", # IP from client
        "history_buffer": "fff0" # Hexadecimal representation of everything the client send
    }
"""


class LoggingLogic:
    def __init__(self, dbcon):
        self.dbcon = dbcon

    def insert_log(self, profile_id, client_ip, history_buffer):
        """
        Insert a new logging entry.
        """
        log_entry = {
            "timestamp": int(time.time()),
            "profile_id": str(profile_id),
            "client_ip": client_ip,
            "history_buffer": history_buffer.hex()
        }
        return self.dbcon.add_entry(log_entry)
