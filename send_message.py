import asyncio
import socket
import logging
import json
from util import set_keepalive_linux, set_keepalive_win

import configargparse
from dotenv import load_dotenv


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
    logger.debug(decoded_data.strip())
    return decoded_data


async def connect(addr, port):
    sock = socket.create_connection((addr, port))
    # set_keepalive_win(sock)
    set_keepalive_linux(sock)
    return await asyncio.open_connection(sock=sock)


async def authorize(addr, token):
    reader, writer = addr
    await get_message(reader)
    await send_message(token, writer)
    auth_resp = await get_message(reader)

    json_data = json.loads(auth_resp)
    if json_data:
        print(f"Auth success for name {json_data['nickname']}")
        return True
    else:
        print(f"Token is invalid. Try it or register new.")
        return False


async def send_message(message, writer):
    encoded_message = f"{message}\n\n".encode()
    logger.debug(encoded_message)
    writer.write(encoded_message)
    await writer.drain()


async def register(addr, name):
    reader, writer = addr
    await get_message(reader)
    await send_message(name, writer)
    await get_message(reader)
    data = await get_message(reader)
    token = json.loads(data)
    print(f"Save this token {token}. And login with it!")


async def main(addr, port, token=None, nickname=None, message=None):
    reader, writer = await connect(addr, port)
    while True:
        if token:
            status = await authorize((reader, writer), token)
            if status:
                await send_message(message, writer)
                break
            else:
                return
        else:
            await register((reader, writer), nickname)
            return


if __name__ == '__main__':
    load_dotenv()
    config = configargparse.ArgParser()
    config.add_argument("--host", help="Chat server host", env_var="HOST")
    config.add_argument("--port", help="Chat server port", env_var="PORT_WRITE")
    config.add_argument("--username", help="Username in chat", default="New user")
    config.add_argument("--token", help="Chat user token")
    config.add_argument("--message", help="Message to sent")
    config.add_argument("--log_file", help="Path to log file", env_var="LOG_FILE")
    options = config.parse_args()
    asyncio.run(main(options.host, options.port, options.token, options.username, options.message))
