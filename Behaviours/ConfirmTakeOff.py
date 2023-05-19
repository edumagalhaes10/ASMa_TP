from spade.behaviour import CyclicBehaviour
from spade.message import Message
from UtilsAirport.PlaneInfo import PlaneInfo
from UtilsAirport.HangarInfo import HangarInfo


#MAYBE MUDAR PARA ONE SHOT E RECEBER MSGS NO LISTENER
# FALTA ADICIONAR PERFORMATIVES

class ConfirmTakeOff(CyclicBehaviour):
    async def run(self):
        # Wait for a message granting or denying permission to take off
        msg = await self.receive()
        if msg:
            # Process the response
            performative = msg.get_metadata('performative')
            if performative == "request":

                body = msg.body.split(" > ")

                req = body[0]
                if req == "Permission to take off?":
                    # hangar_occupation = self.agent.get(f"CargoHangarsOccupied")
                    # print(f"HANGAR OCCUPATION ============CargoHangarsOccupied", hangar_occupation)
                    # hangar_occupation = self.agent.get(f"CommercialHangarsOccupied")
                    # print(f"HANGAR OCCUPATION ============CommercialHangarsOccupied", hangar_occupation)
                    pl_info = body[1].split(" | ")
                    plane_info = []
                    for pl in pl_info:
                        aux = pl.split(": ")
                        plane_info.append(aux[1].strip())

                    pl_info = PlaneInfo(plane_info)

                    # print("HANGAR PLANE THAT WANTS TO TAKE OFF = ",body)
                    info_hangar = body[2].split(" | ")
                    for i,x in enumerate(info_hangar):
                        if i==0:
                            hangar_id = x.split(": ")[1]
                        elif i==1:
                            posx = x.split(": ")[1]
                        elif i==2:
                            posy = x.split(": ")[1]

                    hangar_info = HangarInfo([hangar_id, posx, posy])
                    pl_info.setHangar(hangar_info)

                    # print("HANGAR INFO ===", pl_info.get_hangar())

                    list_free_tracks = self.agent.any_free_track()

                    if len(list_free_tracks)>0:

                        track = self.agent.choose_track_to_takeOff(pl_info, posx, posy)

                        # print("TRACK CHOSEN ========= ", track)
                        # self.agent.get("landingTrack")[0].set_available(False) 
                        # # self.agent.set("planeInOperation",(str(msg.sender),"Take Off"))
                        # self.agent.set("planeInOperation",(pl_info,"Taking Off"))
                        # print(f"Permission to take off received - {str(msg.sender)}")
                        # FALTA PERFORMATIVE
                        response = Message(to=str(msg.sender))
                        response.body = "Permission to take off granted"


                        hangar_occupation = self.agent.get(f"{pl_info.get_type()}HangarsOccupied")
                        # print(f"HANGAR OCCUPATION ============{pl_info.get_type()}HangarsOccupied", hangar_occupation)
                        if hangar_occupation > 0:
                            self.agent.set(f"{pl_info.get_type()}HangarsOccupied", hangar_occupation-1)
                        clear_hangar = Message(to=self.agent.get("hangar_manager"))
                        clear_hangar.body = f"{str(msg.sender)} > Leaving Hangar"
                        # PERFORMATIVE
                        clear_hangar.set_metadata("performative", "inform")
                        await self.send(clear_hangar)
                        await self.send(response)


                    elif len(list_free_tracks)==0:
                        # self.agent.get("takeOffQueue").append(str(msg.sender))
                        # self.agent.get("Queue").append(str(msg.sender))
                        # info = (str(msg.sender), "Waiting To Take Off")
                        info = (pl_info, "Waiting To Take Off")
                        self.agent.get("Queue").append(info)

                        print(f"Permission to take off received - {str(msg.sender)}")
                        response = Message(to=str(msg.sender))
                        response.body = "Permission to take off denied, added to a queue"
                        await self.send(response)


    

   