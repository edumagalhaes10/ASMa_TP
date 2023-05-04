from spade.behaviour import CyclicBehaviour
from spade.message import Message

class ConfirmTakeOff(CyclicBehaviour):
    async def run(self):
        # Wait for a message granting or denying permission to take off
        msg = await self.receive()
        if msg:
            # Process the response
            performative = msg.get_metadata('performative')
            if performative == "request":
                if msg.body == "Permission to take off?"  and self.agent.get("landingTrack").get_available() == True:
                    self.agent.get("landingTrack").set_available(False) 
                    self.agent.set("planeInOperation",(str(msg.sender),"Take Off"))
                    print(f"Permission to take off received - {str(msg.sender)}")
                    response = Message(to=str(msg.sender))
                    response.body = "Permission to take off granted"
                    await self.send(response)


                elif msg.body == "Permission to take off?" and self.agent.get("landingTrack").get_available() == False:
                    self.agent.get("takeOffQueue").append(str(msg.sender))
                    print(f"Permission to take off received - {str(msg.sender)}")
                    response = Message(to=str(msg.sender))
                    response.body = "Permission to take off denied, added to a queue"
                    await self.send(response)


    

   