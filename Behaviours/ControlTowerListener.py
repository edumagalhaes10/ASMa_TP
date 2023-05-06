from spade.behaviour import CyclicBehaviour
from spade.message import Message
import re
from Behaviours.InformTakeOff import InformTakeOff
from Behaviours.InformLanding import InformLanding

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
                    if len(self.agent.get("takeOffQueue")) > 0:
                        newtakeoff = self.agent.get("takeOffQueue")[0]
                        self.agent.set("planeInOperation",(newtakeoff,"Take Off"))
                        self.agent.get("takeOffQueue").pop(0)
                        infoToTakeOff = InformTakeOff()
                        self.agent.add_behaviour(infoToTakeOff)

                elif msg.body=="Landing Completed":
                    print("RECEIVED - ",str(msg.body))
                    self.agent.set("planeInOperation",("",""))
                    self.agent.get("landingTrack").set_available(True) 
                    # TEMOS QUE VERIFICAR OS HANGARS LIVRES 
                    if len(self.agent.get("landingQueue")) > 0:
                        newlanding = self.agent.get("landingQueue")[0]
                        self.agent.set("planeInOperation",(newlanding,"Landing"))
                        self.agent.get("landingQueue").pop(0)
                        infoToLand = InformLanding()
                        self.agent.add_behaviour(infoToLand)

                elif re.match("Hangars Info\n", str(msg.body)):
                    print("RECEIVED HANGARS INFO -", str(msg.body))


            elif performative == "request":
                if msg.body=="Flights Info":
                    print(str(msg.body))
                    reply_msg = msg.make_reply()
                    # reply_msg = Message(to=str(msg.sender))
    
                    reply_msg.body = f"Flights Info Given:\n      Landing: {self.agent.get('landingQueue')} |\n      Taking Off: {self.agent.get('takeOffQueue')} |\n      Plane In Operation: {self.agent.get('planeInOperation')} |\n"
                    reply_msg.set_metadata("performative", "inform")
                    await self.send(reply_msg)
            
            elif performative == "confirm":
                print("CONTROL TOWER RECEIVED HANGAR INFO: ", msg.body)
                body = msg.body.split(" > ")
                id = body[1].strip()
                if body[0] == "There is no free hangar, added to a queue.":
                    self.agent.get("landingQueue").append(id)
                    response = Message(to=id)
                    response.body = "Permission to land denied, added to a queue"
                    await self.send(response)
                else:
                    self.agent.get("landingTrack").set_available(False) 
                    self.agent.set("planeInOperation",(id,"Landing"))
                    response = Message(to=id)
                    response.body = f"Permission to land granted | Hangar = {body[0]}" # PASSAR PISTA E HANGAR
                    #SET PERFORMATIVE
                    await self.send(response)
                # A quem mandar mensagem?????? como guardar isso??


            

   