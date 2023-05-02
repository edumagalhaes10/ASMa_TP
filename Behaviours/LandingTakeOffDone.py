from spade.behaviour import OneShotBehaviour
from spade.message import Message

class LandingTakeOffDone(OneShotBehaviour):
    async def run(self):
        await self.agent.behav.join()
        dest = self.get("control_tower")
        response = Message(to=dest)
        response.body = "Left Track"
      
    

   