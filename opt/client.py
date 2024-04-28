import aiohttp
import asyncio
import json

async def stream_chat():
    url = "http://127.0.0.1:8000/stream_chat/"
    message = {"content": "朝活部の部長はだれ？"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=message) as response:
            if response.status == 200:
                # response.content.iter_any() を使用して任意のバイト数を読み取り
                async for chunk in response.content.iter_any():
                # async for chunk in response.content.iter_chunked(1024):
                    if chunk:
                        text = chunk.decode('utf-8')
                        for char in text:
                            print(char, end='', flush=True)
                    else:
                        print("Received empty chunk")
                    # text = chunk.decode('utf-8')
                    # # print(text, end='')
                    # for char in text:
                    #     print(char, end='', flush=True)
            else:
                print("Failed to connect:", response.status)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # loop = asyncio.get_running_loop()
    loop.run_until_complete(stream_chat())
