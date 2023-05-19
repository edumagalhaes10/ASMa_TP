from spade.behaviour import OneShotBehaviour
from spade.message import Message

class ConfirmLanding(OneShotBehaviour):

    def __init__(self, id, msg, performative):
        self.id = str(id)
        self.msg = str(msg)
        self.perf = str(performative)

        super().__init__()


    async def run(self):

        response = Message(to=self.id)
        response.body = self.msg
        response.set_metadata("performative",self.perf)
        await self.send(response)
  
