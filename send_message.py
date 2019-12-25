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
    # Settings to debug Connection Reset and etc (See more in util.py).
    # Use version depends on platform
    # set_keepalive_win(sock)
    set_keepalive_linux(sock)
    return await asyncio.open_connection(sock=sock)


async def authorize(addr, token):
    reader, writer = addr
    await get_message(reader)
    await send_message(writer, message=token)
    auth_resp = await get_message(reader)

    json_data = json.loads(auth_resp)
    if json_data:
        return json_data['nickname']
    else:
        return None


async def send_message(writer, message="", mtype='service'):
    clean_message = message.replace("\\n", "")
    if mtype == 'message':
        encoded_message = f"{clean_message}\n\n".encode()
    else:
        encoded_message = f"{clean_message}\n".encode()
    logger.debug(encoded_message)
    writer.write(encoded_message)
    await writer.drain()


async def register(addr, name):
    reader, writer = addr
    await get_message(reader)
    await send_message(writer)
    await get_message(reader)
    await send_message(writer, message=name)
    data = await get_message(reader)
    token = json.loads(data)
    return token


async def main(addr, port, token=None, nickname=None, message=None):
    reader, writer = await connect(addr, port)
    while True:
        if token:
            nickname = await authorize((reader, writer), token)
            if nickname:
                print(f"Auth success for name {nickname}")
                await send_message(writer, message=message, mtype="message")
                return
            else:
                print(f"Token is invalid. Check it or register new.")
                return
        else:
            token = await register((reader, writer), nickname)
            if token:
                print(f"Save this token {token}. And login with it!")
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
