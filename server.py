from cor.api import CORModule, Message
import asyncio
import websockets
import json


def pack_msg(message):
	pdict = {"TOPIC": message.atype, "PAYLOAD": message.payload}
	return pdict


def unpack_msg(pdict):
	return Message(pdict["TOPIC"], pdict["PAYLOAD"])


class WebSocketServer(CORModule):
	moduleID = "com.bahus.WebSocketServer"

	async def message_rx(self, message):
		msg_to_send = json.dumps(pack_msg(message))
		for cs in self.clients.keys():
			await self.clients[cs].send(msg_to_send)

	async def ws_rx(self, websocket, path):
		self.clients[websocket.remote_address[0]] = websocket
		while True:
			data_in = await websocket.recv()
			print("Server: " + data_in)
			msg_rx = unpack_msg(json.loads(data_in))
			await self.messageout(msg_rx)

	def __init__(self, network_adapter=None, port=8889, *args, **kwargs):
		super().__init__(network_adapter, *args, **kwargs)
		self.add_topics({"ANY": self.message_rx})
		self.server = websockets.serve(self.ws_rx, '0.0.0.0', port)
		self.clients = {}
		asyncio.get_event_loop().run_until_complete(self.server)


class WebSocketClient(CORModule):
	moduleID = "com.bahus.WebSocketClient"

	def message_rx(self, message):
		msg_to_send = json.dumps(pack_msg(message))
		print(message)
		if self.websocket is not None:
			self.websocket.send(msg_to_send)

	async def ws_rx(self):
		async with websockets.connect("ws://{}:{}".format(self.server, self.port)) as websocket:
			self.websocket = websocket
			while True:
				data_in = await websocket.recv()
				print("Client: " + data_in)
				msg_rx = unpack_msg(json.loads(data_in))
				self.messageout(msg_rx)

	def __init__(self, network_adapter=None, server="localhost", port=8889, *args, **kwargs):
		super().__init__(network_adapter, *args, **kwargs)
		self.add_topics({"ANY": self.message_rx})
		self.server = server
		self.port = port
		self.websocket = None
		asyncio.get_event_loop().run_until_complete(self.ws_rx())