from spade.behaviour import TimeoutBehaviour
from spade.message import Message

class LandingCompleted(TimeoutBehaviour):
    async def run(self):
        msg = Message(to=self.agent.get("control_tower"))
        msg.body = "Landing Completed"
        msg.set_metadata("performative", "inform")
        await self.send(msg)

