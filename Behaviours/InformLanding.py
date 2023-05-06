from spade.behaviour import OneShotBehaviour
from spade.message import Message

class InformLanding(OneShotBehaviour):
    async def run(self):
        msg = Message(to=str(self.agent.get("planeInOperation")[0]))
        msg.body = "Permission to land granted"
        msg.set_metadata("performative", "inform") # N sei se está bem
        await self.send(msg)

