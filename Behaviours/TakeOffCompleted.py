from spade.behaviour import TimeoutBehaviour
from spade.message import Message

class TakeOffCompleted(TimeoutBehaviour):
    async def run(self):
        msg = Message(to=self.agent.get("control_tower"))
        msg.body = f"Take Off Completed > {self.agent.get('jid')}"
        msg.set_metadata("performative", "inform")
        await self.send(msg)
        await self.agent.stop()

