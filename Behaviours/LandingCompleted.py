from spade.behaviour import TimeoutBehaviour
from spade.message import Message

class LandingCompleted(TimeoutBehaviour):
    async def run(self):
        msg = Message(to=self.agent.get("control_tower"))
        msg.body = f"Landing Completed > {self.agent.get('jid')}"
        msg.set_metadata("performative", "inform")
        await self.send(msg)

