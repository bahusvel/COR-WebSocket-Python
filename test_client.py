from cor.api import CORModule, Message
from server import WebSocketClient, WebSocketServer
import threading
import time


class Requester(CORModule):

	moduleID = "com.bahus.Requester"

	def sender(self):
		while True:
			time.sleep(1)
			self.messageout(Message("REQUEST", "IS IT OK?"))

	def acknowledge(self, message):
		print(message)

	def __init__(self, network_adapter=None, *args, **kwargs):
		super().__init__(network_adapter, *args, **kwargs)
		self.add_topics({"RESPONSE": self.acknowledge})
		self.t = threading.Thread(target=self.sender)
		self.t.start()


requester = Requester()
client = WebSocketClient()
requester.network_adapter.register_callback("REQUEST", client)
client.network_adapter.register_callback("RESPONSE", requester)
print("setup done")
time.sleep(50)