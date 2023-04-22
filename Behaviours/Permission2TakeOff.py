from spade.behaviour import OneShotBehaviour
from spade.message import Message

class Permission2TakeOff(OneShotBehaviour):
    async def run(self):
        print("Permission to take off?")
        msg = Message(to=self.agent.get("control_tower"))
        msg.body = "Permission to take off?"
        # msg.set_metadata("performative", "request")
        await self.send(msg)

