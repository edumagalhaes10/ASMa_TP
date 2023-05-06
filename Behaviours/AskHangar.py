from spade.behaviour import OneShotBehaviour
from spade.message import Message

class AskHangar(OneShotBehaviour):
    def __init__(self, sender):
        self.sender = sender
        super().__init__()

    async def run(self):
        msg = Message(to=self.agent.get("hangar_manager"))
        msg.body = f"Is there any free hangar? > {self.sender}"
        msg.set_metadata("performative", "request")
        await self.send(msg)

