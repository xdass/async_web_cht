import asyncio


async def get_message(reader):
    data = await asyncio.wait_for(reader.readline(), timeout=30)
    decoded_data = data.decode()
    return decoded_data


async def connect(addr, port):
    try:
        reader, writer = await asyncio.open_connection(addr, port)
        while True:
            data = await get_message(reader)
            print(f"Recieved: {data}")
    except ConnectionRefusedError:
        print("Refuse")
    except ConnectionResetError:
        print("Reset")
        # reader, writer = await asyncio.open_connection(addr, port)
    finally:
        writer.close()

if __name__ == '__main__':
    asyncio.run(connect("minechat.dvmn.org", 5000))