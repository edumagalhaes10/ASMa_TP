from spade.behaviour import CyclicBehaviour
from spade.message import Message
import datetime 
from Behaviours.TakeOffCompleted import TakeOffCompleted
from Behaviours.LandingCompleted import LandingCompleted
from Behaviours.Cancel import Cancel
from UtilsAirport.HangarInfo import HangarInfo
from Behaviours.Permission2TakeOff import Permission2TakeOff

class PlaneListener(CyclicBehaviour):
    async def run(self):
        response = await self.receive()
        if response:
            performative = response.get_metadata('performative')

            if performative == "inform":
                aux = response.body.split(" > ")
                hangar_info = aux[1].split(" | ")
                arr_info_hangar = []
                for a in hangar_info:
                    aux2 = a.split(": ")
                    arr_info_hangar.append(aux2[1])
                
                info_hangar = HangarInfo(arr_info_hangar)
                self.agent.set("Hangar", info_hangar)   

                permission2TakeOff = Permission2TakeOff()
                self.agent.add_behaviour(permission2TakeOff)


            else:
                body = response.body.split(" | ")

                if body[0] == "Permission to take off granted":
                    print("Almost Taking Off")
                    start_At = datetime.datetime.now() + datetime.timedelta(seconds=15)
                    confirmation = TakeOffCompleted(start_at=start_At)
                    self.agent.add_behaviour(confirmation)
                elif body[0] == "Permission to take off denied, added to a queue":
                    print("Permission to take off denied /////////////////////////////")


                if body[0] == "Permission to land granted":
                    print("Almost Landing")
                    start_At = datetime.datetime.now() + datetime.timedelta(seconds=15)
                    confirmation = LandingCompleted(start_at=start_At)
                    self.agent.add_behaviour(confirmation)
                    self.agent.set("landingTrack", body[2].strip())

                    aux = body[1].split(" / ")
                    arr_info_hangar = []
                    for a in aux:
                        aux2 = a.split(": ")
                        arr_info_hangar.append(aux2[1])
                    
                    info_hangar = HangarInfo(arr_info_hangar)

                    self.agent.set("Hangar", info_hangar)   

                    self.agent.set("Track", body[2].strip())                 

                    # Remove the "Cancel" behavior if it exists
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
            
            
    
    async def on_end(self):
        await self.agent.stop()