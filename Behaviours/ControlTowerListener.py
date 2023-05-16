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
                if msg.body=="Take Off Completed":
                    print("RECEIVED - ",str(msg.body))
                    self.agent.set("planeInOperation",("",""))
                    self.agent.get("landingTrack").set_available(True) 
                    if len(self.agent.get("Queue")) > 0:
                        # 1 A 1 A VER SE PODE DESCOLAR / ATERRAR
                        for i,pl in enumerate(self.agent.get("Queue")):
                            type = pl[0].get_type()
                            print("AGENT HANGAR CAPACITY - ", self.agent.get(f"{type} hangars")) 


                            if pl[1]=="Waiting To Take Off" and self.agent.get("landingTrack").get_available() == True: 
                                self.agent.set("planeInOperation",(pl[0],"Taking Off"))
                                self.agent.get("Queue").pop(i)
                                hangar_occupation = self.agent.get(f"{type}HangarsOccupied")
                                if hangar_occupation > 0:
                                    self.agent.set(f"{type}HangarsOccupied", hangar_occupation-1)
                                infoToTakeOff = InformTakeOff()
                                self.agent.add_behaviour(infoToTakeOff)
                                break
                            elif pl[1]=="Waiting To Land" and self.agent.get("landingTrack").get_available() == True and self.agent.get(f"{type}HangarsOccupied") < self.agent.get(f"{type} hangars"): 
                                hangar_occupation = self.agent.get(f"{type}HangarsOccupied")
                                self.agent.set(f"{type}HangarsOccupied", hangar_occupation+1)
                                askhangar = AskHangar(pl[0])
                                self.agent.add_behaviour(askhangar)
                                break
                    # if len(self.agent.get("takeOffQueue")) > 0:
                    #     newtakeoff = self.agent.get("takeOffQueue")[0]
                    #     self.agent.set("planeInOperation",(newtakeoff,"Take Off"))
                    #     self.agent.get("takeOffQueue").pop(0)
                    #     infoToTakeOff = InformTakeOff()
                    #     self.agent.add_behaviour(infoToTakeOff)

                elif msg.body=="Landing Completed":
                    print("RECEIVED - ",str(msg.body))
                    self.agent.set("planeInOperation",("",""))
                    self.agent.get("landingTrack").set_available(True) 
                    # TEMOS QUE VERIFICAR OS HANGARS LIVRES !!!!!
                    # N sei se deva parar de percorrer logo o ciclo
                    for i,pl in enumerate(self.agent.get("Queue")):
                        type = pl[0].get_type()
                        if pl[1]=="Waiting To Take Off" and self.agent.get("landingTrack").get_available() == True: 
                            self.agent.set("planeInOperation",(pl[0],"Taking Off"))
                            self.agent.get("Queue").pop(i)
                            hangar_occupation = self.agent.get(f"{type}HangarsOccupied")
                            if hangar_occupation > 0:
                                self.agent.set(f"{type}HangarsOccupied", hangar_occupation-1)
                            infoToTakeOff = InformTakeOff()
                            self.agent.add_behaviour(infoToTakeOff)
                            break
                        elif pl[1]=="Waiting To Land" and self.agent.get("landingTrack").get_available() == True and self.agent.get(f"{type}HangarsOccupied") < self.agent.get(f"{type} hangars"): 
                            hangar_occupation = self.agent.get(f"{type}HangarsOccupied")
                            self.agent.set(f"{type}HangarsOccupied", hangar_occupation+1)
                            askhangar = AskHangar(pl[0])
                            self.agent.add_behaviour(askhangar)
                            break
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
                    print("RECEIVED HANGARS INFO -", body)

                    # print("RECEIVED HANGARS INFO -", str(msg.body))


            elif performative == "request":
                if msg.body=="Flights Info":
                    print(str(msg.body))
                    reply_msg = msg.make_reply()
                    # reply_msg = Message(to=str(msg.sender))
                    queue = ""
                    for i,q in enumerate(self.agent.get("Queue")):
                        plane_str = q[0].__str__()
                        # print("TYPEEEEEE", type)
                        q = (plane_str, q[1])
                        queue += "    " + str(i) + ". " + str(q) + " $ " 

                    # print("????????????????QUEUE???? ->, ",queue)


                    reply_msg.body = f"Commercial Hangars> {self.agent.get('Commercial hangars')} \n Commercial Hangars Occupied> {self.agent.get('CommercialHangarsOccupied')} \n Cargo Hangars> {self.agent.get('Cargo hangars')} \n Cargo Hangars Occupied> {self.agent.get('CargoHangarsOccupied')} \n Airport Queue> {queue} \n Plane In Operation> {self.agent.get('planeInOperation')}"  
                    #Taking Off: {self.agent.get('takeOffQueue')} |\n      Plane In Operation: {self.agent.get('planeInOperation')} |\n"
                    reply_msg.set_metadata("performative", "inform")
                    await self.send(reply_msg)
            
            elif performative == "confirm":
                print("CONTROL TOWER RECEIVED HANGAR INFO: ", msg.body)
                body = msg.body.split(" > ")
                id = body[1].strip()
                if body[0] == "There is no free hangar, added to a queue.":
                    if id not in [pl[0] for pl in self.agent.get("Queue")]:
                        self.agent.get("Queue").append(id)
                        response = Message(to=id)
                        response.body = "Permission to land denied, added to a queue"
                        await self.send(response)
                else:
                    self.agent.get("landingTrack").set_available(False) 
                    # index_info = [(i, pl) for i, pl in enumerate(self.agent.get("Queue")) if id == pl[0].get_jid()]

                    index_id = [i for i, pl in enumerate(self.agent.get("Queue")) if id == pl[0].get_jid()]
                    index_plane = [pl for pl in self.agent.get("Queue") if id == pl[0].get_jid()]

                    print("IIIIIIIIIIIIIINDEXXXXXXXXXXXXXXXXXXXXXX ", index_id)
                    if index_id:
                        index_id = index_id[0]
                        print(" !!!!! INDEX ID: ", index_id)
                        plane_info = self.agent.get("Queue")[index_id]
                        self.agent.get("Queue").pop(index_id)
                        # infoToLand = InformLanding()
                        # self.agent.add_behaviour(infoToLand)

                    self.agent.set("planeInOperation",(id,"Landing"))
                    response = Message(to=id)
                    response.body = f"Permission to land granted | Hangar = {body[0]}" # PASSAR PISTA E HANGAR
                    #SET PERFORMATIVE
                    await self.send(response)
                    
                # A quem mandar mensagem?????? como guardar isso??


            

   