
import asyncio
import websockets
import json


async def hello():
    uri = "wss://ws-eu.pusher.com/app/d9b03d485c6d62190e94?protocol=7&client=js&version=5.0.3&flash=false"
    async with websockets.connect(uri) as websocket:
        sub = '{"event":"pusher:subscribe","data":{"channel":"hopin-chat-event-SECRET"}}'
        await websocket.send(sub)
        print(f"> {sub}")
        sub = '{"event":"pusher:subscribe","data":{"channel":"hopin-chat-stage-SECRET"}}'
        await websocket.send(sub)
        print(f"> {sub}")

        while True:
            ws_message = await websocket.recv()
            message = json.loads(ws_message)
            if message['event'] == 'pusher_internal:subscription_succeeded':
                print('subscribe success')
            elif message['event'] == 'message':
                message_data = json.loads(message['data'])
                print(f"{message['channel']}> {message_data['user']['name']}: {message_data['body']}")

asyncio.get_event_loop().run_until_complete(hello())

