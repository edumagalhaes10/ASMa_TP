from spade.behaviour import CyclicBehaviour
from spade.message import Message
import re
from Behaviours.InformTakeOff import InformTakeOff
from Behaviours.InformLanding import InformLanding
from Behaviours.AskHangar import AskHangar
from UtilsAirport.PlaneInfo import PlaneInfo


# BUGADO QUANDO PEDE MAIS HANGARES E OS AVIOES ESTAO NA FILA DE ESPERA


class ControlTowerListener(CyclicBehaviour):
    async def run(self):
        # Wait for a message granting or denying permission to take off
        msg = await self.receive()
        if msg:
            performative = msg.get_metadata('performative')
            # Process the response
            if performative == "inform":
                # if re.match("Take Off Completed", str(msg.body)):
                #     print("RECEIVED - ",str(msg.body))
                #     aux = msg.body.split(" > ")
                #     id_plane = aux[1]
                #     self.agent.set("planeInOperation",("",""))
                #     # self.agent.get("landingTrack")[0].set_available(True) 
                #     if len(self.agent.get("Queue")) > 0:
                #         # 1 A 1 A VER SE PODE DESCOLAR / ATERRAR
                #         for i,pl in enumerate(self.agent.get("Queue")):
                #             type = pl[0].get_type()
                #             print("AGENT HANGAR CAPACITY - ", self.agent.get(f"{type} hangars")) 

                #             list_free_tracks = self.agent.any_free_track()

                #             if pl[1]=="Waiting To Take Off" and len(list_free_tracks)>0: 
                #                 self.agent.set("planeInOperation",(pl[0],"Taking Off"))
                #                 self.agent.get("Queue").pop(i)
                #                 hangar_occupation = self.agent.get(f"{type}HangarsOccupied")
                #                 if hangar_occupation > 0:
                #                     self.agent.set(f"{type}HangarsOccupied", hangar_occupation-1)
                #                 infoToTakeOff = InformTakeOff()
                #                 self.agent.add_behaviour(infoToTakeOff)
                #                 break
                #             elif pl[1]=="Waiting To Land" and len(list_free_tracks)>0 and self.agent.get(f"{type}HangarsOccupied") < self.agent.get(f"{type} hangars"): 
                #                 # hangar_occupation = self.agent.get(f"{type}HangarsOccupied")
                #                 # self.agent.set(f"{type}HangarsOccupied", hangar_occupation+1)
                #                 askhangar = AskHangar(pl[0],list_free_tracks)
                #                 self.agent.add_behaviour(askhangar)
                #                 break
                            
                #             elif len(list_free_tracks)==0 or self.agent.get(f"{type}HangarsOccupied") == self.agent.get(f"{type} hangars"): 
                #                 self.agent.free_tracks(None, None, "")
                    # if len(self.agent.get("takeOffQueue")) > 0:
                    #     newtakeoff = self.agent.get("takeOffQueue")[0]
                    #     self.agent.set("planeInOperation",(newtakeoff,"Take Off"))
                    #     self.agent.get("takeOffQueue").pop(0)
                    #     infoToTakeOff = InformTakeOff()
                    #     self.agent.add_behaviour(infoToTakeOff)
                
                if re.match("Landing Completed", str(msg.body)) or re.match("Take Off Completed", str(msg.body)):
                    # if re.match("Take Off Completed", str(msg.body)):
                    #     self.agent.free_used_track(str(msg.sender))
                    
                    print("RECEIVED - ",str(msg.body))
                    aux = msg.body.split(" > ")
                    id_plane = aux[1]
                    # print("OLAAAAAAAAAAAAAAAAAAAA, ID PLANE, ", id_plane)
                    self.agent.set("planeInOperation",("",""))
                    # self.agent.get("landingTrack")[0].set_available(True) 
                    # if re.match("Take Off Completed", str(msg.body)):
                    #     aux = id_plane.get_id()
                    #     self.agent.free_used_track(aux)

                    # else:
                    self.agent.free_used_track(id_plane)
                    # TEMOS QUE VERIFICAR OS HANGARS LIVRES !!!!!
                    # N sei se deva parar de percorrer logo o ciclo
                    if len(self.agent.get("Queue")) > 0:

                        for i,pl in enumerate(self.agent.get("Queue")):
                            type = pl[0].get_type() 
                            list_free_tracks = self.agent.any_free_track()
    
                            if pl[1]=="Waiting To Take Off" and len(list_free_tracks)>0: 
                                # print(self.agent.get("Queue"))
                                self.agent.get("Queue").pop(i)

                                posx,posy = pl[0].get_hangar().get_coords()
                                track = self.agent.choose_track_to_takeOff(pl[0], posx, posy)    
                                # print("TRACK CHOSEN ========= ", track) 
                                # self.agent.get("landingTrack")[0].set_available(False)    
                                # # self.agent.set("planeInOperation",(str(msg.sender),"Take Off"))
                                # self.agent.set("planeInOperation",(pl_info,"Taking Off"))
                                # print(f"Permission to take off received - {str(msg.sender)}") 
                                # FALTA PERFORMATIVE  
                                hangar_occupation = self.agent.get(f"{type}HangarsOccupied")
                                # print(f"HANGAR OCCUPATION ============{type}HangarsOccupied", hangar_occupation)
                                if hangar_occupation > 0:
                                    self.agent.set(f"{type}HangarsOccupied", hangar_occupation-1)
                                infoToTakeOff = InformTakeOff(pl[0])
                                self.agent.add_behaviour(infoToTakeOff)

                                # self.agent.set("planeInOperation",(pl[0],"Taking Off"))
                                # self.agent.get("Queue").pop(i)
                                # hangar_occupation = self.agent.get(f"{type}HangarsOccupied")
                                # if hangar_occupation > 0:
                                #     self.agent.set(f"{type}HangarsOccupied", hangar_occupation-1)
                                # infoToTakeOff = InformTakeOff()
                                # self.agent.add_behaviour(infoToTakeOff)
                                break
                            elif pl[1]=="Waiting To Land" and len(list_free_tracks)>0 and self.agent.get(f"{type}HangarsOccupied") < self.agent.get(f"{type} hangars"): 
                                # hangar_occupation = self.agent.get(f"{type}HangarsOccupied")
                                # self.agent.set(f"{type}HangarsOccupied", hangar_occupation+1)
                                askhangar = AskHangar(pl[0],list_free_tracks)
                                self.agent.add_behaviour(askhangar)
                                break
                            
                            elif len(list_free_tracks)==0 or self.agent.get(f"{type}HangarsOccupied") == self.agent.get(f"{type} hangars"): 
                                self.agent.free_tracks(None, None, "")
    
                    # if len(self.agent.get("landingQueue")) > 0:
                    #     newlanding = self.agent.get("landingQueue")[0]
                    #     self.agent.set("planeInOperation",(newlanding,"Landing"))
                    #     self.agent.get("landingQueue").pop(0)
                    #     infoToLand = InformLanding()
                    #     self.agent.add_behaviour(infoToLand)

                elif re.match("Hangars Info\n", str(msg.body)):
                    body = msg.body.split(" | ") 
                    body[0] = body[0].split("\n ")[1]
                    for b in body:
                        aux = b.split(": ")
                        self.agent.set(str(aux[0]), int(aux[1]))
                    # print("RECEIVED HANGARS INFO -", body)

                    # print("RECEIVED HANGARS INFO -", str(msg.body))
                
                elif msg.body=="Cancel Landing Request":
                    #au = self.agent.get("Queue")[0]
                    # print(self.agent.get("Queue")[0])
                    #print(f"MSG SENDER {msg.sender()} // {au[0].get_jid()}")
                    # print(f"msg sender________________ {msg.sender}")

                    index_id = [i for i, pl in enumerate(self.agent.get("Queue")) if str(msg.sender) == pl[0].get_jid()]
                    if index_id:
                        index_id = index_id[0]
                        self.agent.get("Queue").pop(index_id)
    
                    # print(f"«««««««««««««««««««««««««««««««««««««« BAZEIIIIIII {index_id} »»»»»»»»»»»»»»»»»»»»»»»»»»»»»")

            elif performative == "request":
                if msg.body=="Flights Info":
                    print(str(msg.body))
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
                        else: info = str(track.get_plane()) + " ➡️ " + track.get_state_plane() + " " + str(track.get_available())
                        info_tracks += "    " + track.get_id() + ". " + info + " $ " 

                        

                    reply_msg.body = f"Commercial Hangars> {self.agent.get('Commercial hangars')} \n Commercial Hangars Occupied> {self.agent.get('CommercialHangarsOccupied')} \n Cargo Hangars> {self.agent.get('Cargo hangars')} \n Cargo Hangars Occupied> {self.agent.get('CargoHangarsOccupied')} \n Airport Queue> {queue} \n Plane In Operation> {info_tracks}"  
                    #Taking Off: {self.agent.get('takeOffQueue')} |\n      Plane In Operation: {self.agent.get('planeInOperation')} |\n"
                    reply_msg.set_metadata("performative", "inform")
                    await self.send(reply_msg)
                
                else:
                    response = Message(to=self.agent.get("hangar_manager"))
                    response.body = msg.body
                    response.set_metadata("performative", "request")
                    await self.send(response)

            
            elif performative == "confirm":
                # res = Message(to=self.agent.get(plane))
                #     res.body = f"Hangar Info > {hangar}"
                #     res.set_metadata("performative", "inform")
                print("CONTROL TOWER RECEIVED HANGAR INFO: ", msg.body)
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
                        # self.agent.get("landingTrack")[0].set_available(False) 
                        # index_info = [(i, pl) for i, pl in enumerate(self.agent.get("Queue")) if id == pl[0].get_jid()]
                        index_id = [i for i, pl in enumerate(self.agent.get("Queue")) if id == pl[0].get_jid()]
                        index_plane = [pl for pl in self.agent.get("Queue") if id == pl[0].get_jid()]

                        if index_id:
                            index_id = index_id[0]
                            plane_info = self.agent.get("Queue")[index_id]
                            self.agent.get("Queue").pop(index_id)
                            # infoToLand = InformLanding()
                            # self.agent.add_behaviour(infoToLand)

                        self.agent.set("planeInOperation",(id,"Landing"))
                        
                        hangar = hangar.replace("|", "/")

                        response = Message(to=id)
                        response.body = f"Permission to land granted | {hangar} | {track}" # PASSAR PISTA E HANGAR
                        #SET PERFORMATIVE
                        await self.send(response)
                    


            

   