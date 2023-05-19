from spade.behaviour import OneShotBehaviour
from spade.message import Message

class Add2RandomHangar(OneShotBehaviour):
    def __init__(self, jid, type):
        self.jid = jid
        self.type = type
        super().__init__()

    async def run(self):
        msg = Message(to=self.agent.get("control_tower"))
        msg.body = f"Add to an hangar > {self.jid} > {self.type}"
        msg.set_metadata("performative", "request")
        await self.send(msg)

