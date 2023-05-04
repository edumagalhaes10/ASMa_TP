from spade.behaviour import PeriodicBehaviour
from spade.message import Message
import datetime

class AskFlightInfo(PeriodicBehaviour):
    async def on_start(self):
        self.counter = 0

    async def run(self):

        print(f"Flights Info running at {datetime.datetime.now().time()}: {self.counter}")

        self.counter += 1

        msg = Message(to=self.agent.get("control_tower"))
        msg.body = "Flights Info"
        msg.set_metadata("performative", "request")
        await self.send(msg)

        
    


   