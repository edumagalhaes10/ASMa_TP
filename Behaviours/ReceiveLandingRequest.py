from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Behaviours.AskHangar import AskHangar
from UtilsAirport.PlaneInfo import PlaneInfo
from UtilsAirport.HangarInfo import HangarInfo
from Behaviours.ConfirmLanding import ConfirmLanding


class ReceiveLandingRequest(CyclicBehaviour):
    async def run(self):
        msg = await self.receive()
        if msg:
            performative = msg.get_metadata('performative')
            if performative == "request":
                body = msg.body.split(" > ")
                req = body[0]
                if req == "Permission to land?":
                    pl_info = body[1].split(" | ")
                    plane_info = []
                    for pl in pl_info:
                        aux = pl.split(": ")
                        plane_info.append(aux[1].strip())

                    pl_info = PlaneInfo(plane_info)
                    list_free_tracks = self.agent.any_free_track()
                    self.agent.get("help_structure")[pl_info.get_jid()] = pl_info

                    if len(list_free_tracks) > 0 and self.agent.get(f"{pl_info.get_type()}HangarsOccupied") < self.agent.get(f"{pl_info.get_type()} hangars"):
                        print(f"Permission to land received - {str(msg.sender)}")
                        askhangar = AskHangar(pl_info, list_free_tracks)
                        self.agent.add_behaviour(askhangar)

                    elif (len(list_free_tracks)==0 or self.agent.get(f"{pl_info.get_type()}HangarsOccupied") == self.agent.get(f"{pl_info.get_type()} hangars")) and self.agent.count_planes_waiting2land() < self.agent.get("maxPlanes2Land"):
                        self.agent.free_tracks(None, None, "")
                        hangar_info = HangarInfo(["-", "-", "-"])
                        pl_info.setHangar(hangar_info)

                        info = (pl_info, "Waiting To Land")
                        if self.agent.get(f"{pl_info.get_type()}HangarsOccupied") <= 0.3* self.agent.get(f"{pl_info.get_type()} hangars"):
                            self.agent.get("Queue").insert(0,info)
                        else:
                            self.agent.get("Queue").append(info)

                        print(f"Permission to land received - {str(msg.sender)}")
                        confirmLanding = ConfirmLanding(str(msg.sender), "Permission to land denied, added to a queue", "refuse")
                        self.agent.add_behaviour(confirmLanding)
                    
                    elif self.agent.count_planes_waiting2land() == self.agent.get("maxPlanes2Land"):
                        last = self.get("Canceled Landings")
                        self.set("Canceled Landings", last+1)
                        confirmLanding = ConfirmLanding(str(msg.sender), "Permission to land denied, Landing Queue is full - Must head to Lisboa Airport", "refuse")
                        self.agent.add_behaviour(confirmLanding)