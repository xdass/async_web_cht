import asyncio
import datetime
import time
import socket
from util import set_keepalive_linux

import aiofiles
import configargparse
from dotenv import load_dotenv


async def log_message(message):
    now = datetime.datetime.now()
    formatted_date = now.strftime("%d.%m.%Y %H:%M")
    async with aiofiles.open(options.log_file, "a+", encoding="utf-8") as fh:
        await fh.write(f"[{formatted_date}] {message}")


async def get_message(reader):
    data = await reader.readline()
    decoded_data = data.decode()
    await log_message(decoded_data)
    return decoded_data


async def connect(addr, port):
    sock = socket.create_connection((addr, port))
    set_keepalive_linux(sock)
    return await asyncio.open_connection(sock=sock)


async def main(addr, port):
    connection_attempts = 0
    connection_timeout = 3
    message = f"Connection lost! Retry through {connection_timeout} sec\n"
    while True:
        try:
            reader, writer = await connect(addr, port)
            await log_message("Connection established!\n")
            connection_attempts = 0
            while True:
                await get_message(reader)
        except (ConnectionRefusedError, ConnectionResetError, socket.gaierror):
            await log_message("Connection lost! Trying reconnect.\n" if connection_attempts < 2 else message)
            if connection_attempts >= 2:
                time.sleep(connection_timeout)
            connection_attempts += 1

if __name__ == '__main__':
    load_dotenv()
    config = configargparse.ArgParser()
    config.add_argument("--host", help="Chat server host", env_var="HOST")
    config.add_argument("--port", help="Chat server port", env_var="PORT")
    config.add_argument("--log_file", help="Path to log file", env_var="LOG_FILE")
    options = config.parse_args()
    asyncio.run(main(options.host, options.port))
