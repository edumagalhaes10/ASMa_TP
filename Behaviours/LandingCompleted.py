from spade.behaviour import TimeoutBehaviour
from spade.message import Message
from Behaviours.TimeoutToTakeOff import TimeoutToTakeOff
import datetime

class LandingCompleted(TimeoutBehaviour):
    async def run(self):
        msg = Message(to=self.agent.get("control_tower"))
        msg.body = f"Landing Completed > {self.agent.get('jid')}"
        msg.set_metadata("performative", "inform")
        await self.send(msg)
        
        origin = self.agent.get("Origin")
        destination = self.agent.get("Destination")
        self.agent.set("Origin", destination)
        self.agent.set("Destination", origin)
        self.agent.set("Fuel", 100)
        start_At = datetime.datetime.now() + datetime.timedelta(seconds=15)
        timeout2TakeOff = TimeoutToTakeOff(start_at=start_At)
        self.agent.add_behaviour(timeout2TakeOff)
