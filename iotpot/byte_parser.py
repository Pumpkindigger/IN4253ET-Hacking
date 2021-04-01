import logging

telnet_command_options = {
    0: "Binary Transmission",
    1: "Echo",
    2: "Reconnection",
    3: "Suppress Go Ahead",  # https://tools.ietf.org/html/rfc858
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
    24: "End of Record",  # https://tools.ietf.org/html/rfc885
    26: "TACACS User Identification",
    27: "Output Marking",
    28: "Terminal Location Number",
    29: "Telnet 3270 Regime",
    30: "X.3 PAD",
    31: "Negotiate About Window Size",  # https://tools.ietf.org/html/rfc1073
    32: "Terminal Speed",  # https://tools.ietf.org/html/rfc1079
    33: "Remote Flow Control",  # https://tools.ietf.org/html/rfc1372
    34: "Linemode",  # https://tools.ietf.org/html/rfc1116
    35: "X Display Location",
    36: "Environment Option",
    37: "Authentication Option",
    38: "Encryption Option",
    39: "New Environment Option",  # https://tools.ietf.org/html/rfc1572
    40: "TN3270E",
    41: "XAUTH",
    42: "CHARSET",
    43: "Telnet Remote Serial Port (RSP)",
    44: "Com Port Control Option",
    45: "Telnet Suppress Local Echo",
    46: "Telnet Start TLS",
    47: "KERMIT",
    48: "SEND-URL",
    49: "FORWARD_X",
}

telnet_commands = {
    240: "SE",
    241: "NOP",
    242: "Data Mark",
    243: "BREAK",
    244: "Interrupt Process",
    245: "Abort Output",
    246: "Are You There",
    247: "Erase Character",
    248: "Erase Line",
    249: "Go ahead",
    250: "SB",
    251: "WILL",
    252: "WONT",
    253: "DO",
    254: "DONT",
}


def parse_buffer(buffer, ip):
    i = 0
    commands = []
    text = ""

    while i < len(buffer):
        byte_iac = buffer[i]
        if byte_iac == 255:  # Found an IAC!
            i += 1
            if i >= len(buffer):
                logging.warning(f"FROM {ip} INCOMPLETE IAC.")

            byte_command = buffer[i]
            if byte_command in telnet_commands:  # Found a known command!
                if 250 < byte_command:  # Found a telnet option command!
                    i += 1
                    if i >= len(buffer):
                        logging.warning(f"FROM {ip} INCOMPLETE IAC OPTION.")

                    byte_option = buffer[i]
                    if byte_option in telnet_command_options:  # Found a known option!
                        logging.info(f"FROM {ip} IAC {telnet_commands[byte_command]} : {telnet_command_options[byte_option]}")
                        commands.append([byte_command, byte_option])
                    else:
                        logging.info(f"FROM {ip} IAC {telnet_commands[byte_command]} UNKNOWN OPTION: {telnet_command_options[byte_option]}")
                else:
                    logging.info(f"FROM {ip} IAC {telnet_commands[byte_command]}")

                    command_array = [byte_command]
                    if byte_command == 250:  # Subnegotiation of the indicated option follows.
                        i += 1
                        while not (buffer[i] == 255 and buffer[i + 1] == 240):
                            command_array.append(buffer[i])
                            i += 1
                        i -= 1  # Go one back to allow parsing of IAC SE.
                    commands.append(command_array)
            else:
                logging.warning(f"FROM {ip} INVALID IAC.")
        else:
            text = text + chr(byte_iac)
        i += 1
    return commands, text.rstrip()
