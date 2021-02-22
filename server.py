import asyncio
import telnetlib3

# Telnet RFC https://tools.ietf.org/html/rfc854
# Telnet Options https://www.iana.org/assignments/telnet-options/telnet-options.xhtml


async def shell(reader: telnetlib3.TelnetReader, writer: telnetlib3.TelnetWriter):
    # Telnet options
    linemode = writer.linemode
    received_options = writer.remote_option

    # Welcome message
    writer.write("BCM96318 Broadband Router\r\n")

    # Login prompt
    writer.write("Login: \r\n")

    # Check user/pass
    inp = await reader.readline()
    if inp:
        # Echo input
        writer.echo(inp + '\r\n')
        # For now we always say access granted
        writer.write('Access granted\r\n')

    # Process commands
    while True:
        # This is placeholder for now
        inp = await reader.readline()
        if "close" not in inp:
            writer.echo(inp + '\r\n')
        else:
            # Closes the connection
            writer.close()


loop = asyncio.get_event_loop()
coro = telnetlib3.create_server(port=6023, shell=shell)
server = loop.run_until_complete(coro)
loop.run_until_complete(server.wait_closed())
