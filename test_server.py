from cor.api import CORModule, Message
from server import WebSocketClient, WebSocketServer
import time

class Responder(CORModule):

	moduleID = "com.bahus.Responder"

	def response(self, message):
		print(message)
		self.messageout(Message("RESPONSE", "ITS ALRIGHT"))

	def __init__(self, network_adapter=None, *args, **kwargs):
		super().__init__(network_adapter, *args, **kwargs)
		self.add_topics({"REQUEST": self.response})


responder = Responder()
server = WebSocketServer()
print("Server laucnhed")
responder.network_adapter.register_callback("RESPONSE", server)
server.network_adapter.register_callback("REQUEST", responder)
print("callbacks registered")
time.sleep(50)