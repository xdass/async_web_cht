import asyncio
import socket
import time
import logging

import configargparse
from dotenv import load_dotenv

USER_TOKEN = "291f0cba-1e7d-11ea-b989-0242ac110002"
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


async def get_message(reader):
    data = await reader.readline()
    decoded_data = data.decode()
    # print(decoded_data)
    return decoded_data


async def connect(addr, port):
    sock = socket.create_connection((addr, port))
    sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 10000, 3000))
    return await asyncio.open_connection(sock=sock)


async def auth(token, writer):
    encoded_message = token.encode() + b"\n"
    logger.debug(encoded_message)
    writer.write(encoded_message)
    await writer.drain()


async def send_message(message, writer):
    encoded_message = message.encode() + b"\n\n"
    logger.debug(encoded_message)
    writer.write(encoded_message)
    await writer.drain()


async def main(addr, port):
    connection_attempts = 0
    connection_timeout = 3
    message = f"Connection lost! Retry through {connection_timeout} sec\n"
    while True:
        try:
            reader, writer = await connect(addr, port)
            # await log_message("Connection established!\n")
            connection_attempts = 0
            while True:
                data = await get_message(reader)
                logger.debug(data)
                if data.strip() == "Hello %username%! Enter your personal hash or leave it empty to create new account.":
                    await auth(USER_TOKEN, writer)
                elif data.strip() == "Welcome to chat! Post your message below. End it with an empty line.":
                    await send_message("Test message Devman", writer)
                # await log_message(data)
        except (ConnectionRefusedError, ConnectionResetError, socket.gaierror):
            # await log_message("Connection lost! Trying reconnect.\n" if connection_attempts < 2 else message)
            if connection_attempts >= 2:
                time.sleep(connection_timeout)
            connection_attempts += 1

if __name__ == '__main__':
    # load_dotenv()
    config = configargparse.ArgParser()
    config.add_argument("--host", help="Chat server host", env_var="HOST")
    config.add_argument("--port", help="Chat server port", env_var="PORT")
    config.add_argument("--log_file", help="Path to log file", env_var="LOG_FILE")
    options = config.parse_args()
    print(config.format_values())
    asyncio.run(main("minechat.dvmn.org", 5050))