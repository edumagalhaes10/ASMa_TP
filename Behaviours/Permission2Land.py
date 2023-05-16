from spade.behaviour import OneShotBehaviour
from spade.message import Message

class Permission2Land(OneShotBehaviour):
    async def run(self):
        print("Permission to land")
        msg = Message(to=self.agent.get("control_tower"))
        msg.body = f"Permission to land? > {self.agent.__str__()}"
        msg.set_metadata("performative", "request")
        await self.send(msg)

