from spade.behaviour import TimeoutBehaviour
from spade.message import Message

class TakeOffCompleted(TimeoutBehaviour):
    async def run(self):
        msg = Message(to=self.agent.get("control_tower"))
        msg.body = "Take Off Completed"
        msg.set_metadata("performative", "inform")
        await self.send(msg)

