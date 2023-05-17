from spade.behaviour import TimeoutBehaviour
from spade.message import Message

class Cancel(TimeoutBehaviour):

    async def run(self):
        if self.agent.get("flag") == True:
            msg = Message(to=self.agent.get("control_tower"))
            msg.body = f"Cancel Landing Request"
            msg.set_metadata("performative", "inform")
            await self.send(msg)
            await self.agent.stop()
