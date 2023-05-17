from spade.behaviour import CyclicBehaviour
from spade.message import Message
import datetime 
from Behaviours.TakeOffCompleted import TakeOffCompleted
from Behaviours.LandingCompleted import LandingCompleted
from Behaviours.Cancel import Cancel

class PlaneListener(CyclicBehaviour):
    async def run(self):
        response = await self.receive()
        if response:
            print("RESPONSE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!: ",response.body)
            body = response.body.split(" | ")
            print("SPLIT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!: ",body)

            if body[0] == "Permission to take off granted":
                print("Almost Taking Off")
                start_At = datetime.datetime.now() + datetime.timedelta(seconds=30)
                confirmation = TakeOffCompleted(start_at=start_At)
                self.agent.add_behaviour(confirmation)
            elif body[0] == "Permission to take off denied, added to a queue":
                print("Permission to take off denied /////////////////////////////")

            
            if body[0] == "Permission to land granted":
                print("Almost Landing")
                start_At = datetime.datetime.now() + datetime.timedelta(seconds=15)
                confirmation = LandingCompleted(start_at=start_At)
                self.agent.add_behaviour(confirmation)
                # Remove the "Cancel" behavior if it exists
                print("<<<<< LISTA BEHAVS: ", self.agent.behaviours)
                # for behaviour in self.agent.behaviours:
                #     if isinstance(behaviour, Cancel):
                #         # behaviour.kill()
                #         behaviour.cancel()
                #         self.agent.remove_behaviour(behaviour)
                #         print("<<<<< CANCEL BEHAVIOR KILLED AND REMOVED >>>>>")
                self.agent.set("flag", False)
                

            elif body[0] == "Permission to land denied, added to a queue":
                start_At = datetime.datetime.now() + datetime.timedelta(seconds=50)
                cancel = Cancel(start_at=start_At)
                self.agent.add_behaviour(cancel)
                print("Permission to land denied /////////////////////////////")
    
    async def on_end(self):
        await self.agent.stop()