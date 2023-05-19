from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Behaviours.AskHangar import AskHangar
from UtilsAirport.PlaneInfo import PlaneInfo

class ConfirmLanding(CyclicBehaviour):
    async def run(self):
        # Wait for a message granting or denying permission to land
        msg = await self.receive()
        if msg:
            performative = msg.get_metadata('performative')
            if performative == "request":
                body = msg.body.split(" > ")
                # print("INFO PLANE -> " , body)

                req = body[0]
                if req == "Permission to land?":
                    pl_info = body[1].split(" | ")
                    plane_info = []
                    for pl in pl_info:
                        aux = pl.split(": ")
                        plane_info.append(aux[1].strip())

                    pl_info = PlaneInfo(plane_info)
                    list_free_tracks = self.agent.any_free_track()
                    # print("FREE TRACKS: ", list_free_tracks)

                    if len(list_free_tracks)>0 and self.agent.get(f"{pl_info.get_type()}HangarsOccupied") < self.agent.get(f"{pl_info.get_type()} hangars"):
                        # self.agent.get("landingTrack")[0].set_available(False) 
                        # self.agent.set("planeInOperation",(str(msg.sender),"Landing"))
                        print(f"Permission to land received - {str(msg.sender)}")

                        # hangar_occupation = self.agent.get(f"{pl_info.get_type()}HangarsOccupied")
                        # self.agent.set(f"{pl_info.get_type()}HangarsOccupied", hangar_occupation+1)

                        # askhangar = AskHangar(str(msg.sender))
                        askhangar = AskHangar(pl_info, list_free_tracks)
                        self.agent.add_behaviour(askhangar)

                        # response = Message(to=str(msg.sender))
                        # response.body = "Permission to land granted"
                        # await self.send(response)

                    elif (len(list_free_tracks)==0 or self.agent.get(f"{pl_info.get_type()}HangarsOccupied") == self.agent.get(f"{pl_info.get_type()} hangars")):
                        # self.agent.get("landingQueue").append(str(msg.sender))
                        # self.agent.get("Queue").append(str(msg.sender))
                        self.agent.free_tracks(None, None, "")


                        # info = (str(msg.sender), "Waiting To Land")
                        info = (pl_info, "Waiting To Land")
                        self.agent.get("Queue").append(info)

                        print(f"Permission to land received - {str(msg.sender)}")
                        response = Message(to=str(msg.sender))
                        response.body = "Permission to land denied, added to a queue"
                        await self.send(response)
