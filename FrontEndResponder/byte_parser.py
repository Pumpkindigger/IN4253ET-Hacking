telnet_command_options = {
    0: "Binary Transmission",
    1: "Echo",
    2: "Reconnection",
    3: "Suppress Go Ahead",
    4: "Approx Message Size Negotiation",
    5: "Status",
    6: "Timing Mark",
    7: "Remote Controlled Trans and Echo",
    8: "Output Line Width",
    9: "Output Page Size",
    10: "Output Carriage-Return Disposition",
    11: "Output Horizontal Tab Stops",
    12: "Output Horizontal Tab Disposition",
    13: "Output Formfeed Disposition",
    14: "Output Vertical Tabstops",
    15: "Output Vertical Tab Disposition",
    16: "Output Linefeed Disposition",
    17: "Extended ASCII",
    18: "Logout",
    19: "Byte Macro",
    20: "Data Entry Terminal",
    21: "SUPDUP",
    22: "SUPDUP Output",
    23: "Send Location",
    24: "End of Record",
    26: "TACACS User Identification",
    27: "Output Marking",
    28: "Terminal Location Number",
    29: "Telnet 3270 Regime",
    30: "X.3 PAD",
    31: "Negotiate About Window Size",
    32: "Terminal Speed",
    33: "Remote Flow Control",
    34: "Linemode",
    35: "X Display Location",
    36: "Environment Option",
    37: "Authentication Option",
    38: "Encryption Option	",
    39: "New Environment Option",
    40: "TN3270E	",
    41: "XAUTH	",
    42: "CHARSET",
    43: "Telnet Remote Serial Port (RSP)	",
    44: "Com Port Control Option	",
    45: "Telnet Suppress Local Echo	",
    46: "Telnet Start TLS	",
    47: "KERMIT	",
    48: "SEND-URL	",
    49: "FORWARD_X",
}

telnet_commands = {
    240: "SE",
    241: "NOP",
    242: "Data Mark",
    243: "Break	",
    244: "Interrupt Process",
    245: "Abort output",
    246: "Are You There",
    247: "Erase character",
    248: "Erase Line",
    249: "Go ahead",
    250: "SB",
    251: "will",
    252: "wont",
    253: "do",
    254: "dont",
}


class ByteParser():
    """Parses the input"""

    def parse_string(self, buffer):
        i = 0;
        while i < len(buffer):
            if buffer[i] == 255:
                i += 1
                if (ByteParser.is_command_code(self, buffer[i])):
                    print(telnet_commands[buffer[i]])
                    i += 1
                    if (ByteParser.is_command_option_code(self, buffer[i])):
                        print(telnet_command_options[buffer[i]])
            else:
                i += 1

    def is_command_code(self, code):
        if (code < 255 and code > 240):
            return True
        else:
            return False

    def is_command_option_code(self, code):
        if (code <= 49):
            return True
        else:
            return False

