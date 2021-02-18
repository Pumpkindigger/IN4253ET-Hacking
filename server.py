import asyncio, telnetlib3

@asyncio.coroutine
def shell(reader, writer):
    # Telnet options
    # TODO no clue yet

    # Welcome message
    writer.write("BCM96318 Broadband Router")

    # Login prompt
    writer.write("\r\nLogin:")

    # Check user/pass
    inp = yield from reader.read(1024)
    if inp:
        # Echo input
        writer.echo(inp)
        # For now we always say acess granted
        writer.write('\r\nAccess granted')
        yield from writer.drain()

    # Process commands
    while True:
        # This is placeholder for now
        inp = yield from reader.read(1024)
        if inp != "close":
            writer.echo(inp)
        else:
            # Closes the connection
            writer.close()


loop = asyncio.get_event_loop()
coro = telnetlib3.create_server(port=6023, shell=shell)
server = loop.run_until_complete(coro)
loop.run_until_complete(server.wait_closed())