from spade.behaviour import CyclicBehaviour
from spade.message import Message
import re
from Behaviours.ConfirmTakeOff import ConfirmTakeOff
from Behaviours.ConfirmLanding import ConfirmLanding
from Behaviours.AskHangar import AskHangar
from UtilsAirport.HangarInfo import HangarInfo
from termcolor import colored



# BUGADO QUANDO PEDE MAIS HANGARES E OS AVIOES ESTAO NA FILA DE ESPERA


class ControlTowerListener(CyclicBehaviour):
    async def run(self):
        msg = await self.receive()
        if msg:
            performative = msg.get_metadata('performative')
            # Process the response
            if performative == "inform":
                
                if re.match("Landing Completed", str(msg.body)) or re.match("Take Off Completed", str(msg.body)):
                    print("RECEIVED - ",str(msg.body))
                    aux = msg.body.split(" > ")
                    id_plane = aux[1]
                    self.agent.set("planeInOperation",("",""))
                    self.agent.free_used_track(id_plane)
                    if len(self.agent.get("Queue")) > 0:

                        for i,pl in enumerate(self.agent.get("Queue")):
                            type = pl[0].get_type() 
                            list_free_tracks = self.agent.any_free_track()
    
                            if pl[1]=="Waiting To Take Off" and len(list_free_tracks)>0: 
                                self.agent.get("Queue").pop(i)

                                posx,posy = pl[0].get_hangar().get_coords()
                                track = self.agent.choose_track_to_takeOff(pl[0], posx, posy)    
                                hangar_occupation = self.agent.get(f"{type}HangarsOccupied")
                                if hangar_occupation > 0:
                                    self.agent.set(f"{type}HangarsOccupied", hangar_occupation-1)
                                infoToTakeOff = ConfirmTakeOff(pl[0])
                                self.agent.add_behaviour(infoToTakeOff)
                                break
                            elif pl[1]=="Waiting To Land" and len(list_free_tracks)>0 and self.agent.get(f"{type}HangarsOccupied") < self.agent.get(f"{type} hangars"): 
                                askhangar = AskHangar(pl[0],list_free_tracks)
                                self.agent.add_behaviour(askhangar)
                                break
                            
                            elif len(list_free_tracks)==0 or self.agent.get(f"{type}HangarsOccupied") == self.agent.get(f"{type} hangars"): 
                                self.agent.free_tracks(None, None, "")
    
                elif re.match("Hangars Info\n", str(msg.body)):
                    body = msg.body.split(" | ") 
                    body[0] = body[0].split("\n ")[1]
                    for b in body:
                        aux = b.split(": ")
                        self.agent.set(str(aux[0]), int(aux[1]))
                
                elif msg.body=="Cancel Landing Request":
                    index_id = [i for i, pl in enumerate(self.agent.get("Queue")) if str(msg.sender) == pl[0].get_jid()]
                    if index_id:
                        index_id = index_id[0]
                        self.agent.get("Queue").pop(index_id)
    

            elif performative == "request":
                if msg.body=="Flights Info":
                    reply_msg = msg.make_reply()
                    queue = ""
                    for i,q in enumerate(self.agent.get("Queue")):
                        plane_str = q[0].__str__()
                        q = (plane_str, q[1])
                        queue += "    " + str(i) + ". " + str(q) + " $ " 

                    
                    info_tracks=""
                    for track in self.agent.get("landingTrack"):
                        if track.get_plane() == None:
                            info = "Empty" + " " + str(track.get_available())
                        else: info = str(track.get_plane()) + " ➡️ " + track.get_state_plane() #+ " " + str(track.get_available())
                        info_tracks += "    " + str(colored(track.get_id(), "yellow")) + ". " + info + " $ " 

                        

                    reply_msg.body = f"Commercial Hangars> {self.agent.get('Commercial hangars')} \n Commercial Hangars Occupied> {self.agent.get('CommercialHangarsOccupied')} \n Cargo Hangars> {self.agent.get('Cargo hangars')} \n Cargo Hangars Occupied> {self.agent.get('CargoHangarsOccupied')} \n Airport Queue> {queue} \n Plane In Operation> {info_tracks}"  
                    reply_msg.set_metadata("performative", "inform")
                    await self.send(reply_msg)
                
                else:
                    response = Message(to=self.agent.get("hangar_manager"))
                    response.body = msg.body
                    response.set_metadata("performative", "request")
                    await self.send(response)

            
            elif performative == "confirm":
                # print("CONTROL TOWER RECEIVED HANGAR INFO: ", msg.body)
                body = msg.body.split(" > ")
                if body[0].strip() == "Initial Hangar":
                    hangar = body[1].strip()
                    plane = body[2].strip()
                    res = Message(to=plane)
                    res.body = f"Hangar Info > {hangar}"
                    res.set_metadata("performative", "inform")
                    await self.send(res)


                else:
                    if len(body) == 4:
                        hangar = body[0].strip()
                        track = body[1].strip()
                        id = body[2].strip()
                        type = body[3].strip()

                        hangar_split =  body[0].split(" | ") 

                        arr_info_hangar = []
                        for a in hangar_split:
                            aux2 = a.split(": ")
                            arr_info_hangar.append(aux2[1])

                        info_hangar = HangarInfo(arr_info_hangar)

                        self.agent.get("help_structure")[id].setHangar(info_hangar)

                    else:
                        id = body[1].strip()

                    if body[0] == "There is no free hangar, added to a queue.":
                        self.agent.free_tracks(None, id, "")

                        if id not in [pl[0] for pl in self.agent.get("Queue")]:
                            self.agent.get("Queue").append(id)
                            response = Message(to=id)
                            response.body = "Permission to land denied, added to a queue"
                            await self.send(response)
                    else:
                        self.agent.free_tracks(track, id, "Landing")
                        hangar_occupation = self.agent.get(f"{type}HangarsOccupied")
                        self.agent.set(f"{type}HangarsOccupied", hangar_occupation+1)
                        index_id = [i for i, pl in enumerate(self.agent.get("Queue")) if id == pl[0].get_jid()]
                        index_plane = [pl for pl in self.agent.get("Queue") if id == pl[0].get_jid()]

                        if index_id:
                            index_id = index_id[0]
                            plane_info = self.agent.get("Queue")[index_id]
                            self.agent.get("Queue").pop(index_id)

                        self.agent.set("planeInOperation",(id,"Landing"))
                        hangar = hangar.replace("|", "/")

                        confirmLanding = ConfirmLanding(id, f"Permission to land granted | {hangar} | {track}", "confirm")
                        self.agent.add_behaviour(confirmLanding)
                    


            

   