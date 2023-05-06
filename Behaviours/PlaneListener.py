from spade.behaviour import CyclicBehaviour
from spade.message import Message
import datetime 
from Behaviours.TakeOffCompleted import TakeOffCompleted
from Behaviours.LandingCompleted import LandingCompleted

class PlaneListener(CyclicBehaviour):
    async def run(self):
        response = await self.receive()
        if response:
            print("RESPONSE: ",response.body)
            body = response.body.split(" | ")
            if response.body == "Permission to take off granted":
                print("Almost Taking Off")
                start_At = datetime.datetime.now() + datetime.timedelta(seconds=30)
                confirmation = TakeOffCompleted(start_at=start_At)
                self.agent.add_behaviour(confirmation)


            elif response.body == "Permission to take off denied":
                print("Permission to take off denied")

            if body[0] == "Permission to land granted":
                print("Almost Landing")
                start_At = datetime.datetime.now() + datetime.timedelta(seconds=15)
                confirmation = LandingCompleted(start_at=start_At)
                self.agent.add_behaviour(confirmation)
            elif response.body == "Permission to land denied":
                print("Permission to land denied")
    
    async def on_end(self):
        await self.agent.stop()