from spade.behaviour import CyclicBehaviour
from spade.message import Message
from UtilsAirport.PlaneInfo import PlaneInfo


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
                print("INFO PLANE -> " , body)

                req = body[0]
                pl_info = body[1].split(" | ")
                plane_info = []
                for pl in pl_info:
                    aux = pl.split(": ")
                    plane_info.append(aux[1].strip())
                    print(">>>>>>>PLANE:", aux[1].strip(), "###")
                
                pl_info = PlaneInfo(plane_info)

                if req == "Permission to take off?"  and self.agent.get("landingTrack").get_available() == True:
                    
                    self.agent.get("landingTrack").set_available(False) 
                    # self.agent.set("planeInOperation",(str(msg.sender),"Take Off"))
                    self.agent.set("planeInOperation",(pl_info,"Taking Off"))
                    print(f"Permission to take off received - {str(msg.sender)}")
                    response = Message(to=str(msg.sender))
                    response.body = "Permission to take off granted"
                    hangar_occupation = self.agent.get(f"{pl_info.get_type()}HangarsOccupied")
                    if hangar_occupation > 0:
                        self.agent.set(f"{pl_info.get_type()}HangarsOccupied", hangar_occupation-1)
                    clear_hangar = Message(to=self.agent.get("hangar_manager"))
                    clear_hangar.body = f"{str(msg.sender)} > Leaving Hangar"
                    # PERFORMATIVE
                    clear_hangar.set_metadata("performative", "inform")
                    await self.send(response)


                elif req == "Permission to take off?" and self.agent.get("landingTrack").get_available() == False:
                    # self.agent.get("takeOffQueue").append(str(msg.sender))
                    # self.agent.get("Queue").append(str(msg.sender))
                    # info = (str(msg.sender), "Waiting To Take Off")
                    info = (pl_info, "Waiting To Take Off")
                    self.agent.get("Queue").append(info)
                    
                    print(f"Permission to take off received - {str(msg.sender)}")
                    response = Message(to=str(msg.sender))
                    response.body = "Permission to take off denied, added to a queue"
                    await self.send(response)


    

   