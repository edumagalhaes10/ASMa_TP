from spade.behaviour import CyclicBehaviour
from spade.message import Message

class ConfirmLanding(CyclicBehaviour):
    #FALTA TIMEOUT 
    async def run(self):
        # Wait for a message granting or denying permission to take off
        msg = await self.receive()
        if msg:
            if msg.body == "Permission to land?" and self.agent.get("landingTrack").get_available() == True:
                self.agent.get("landingTrack").set_available(False) 
                print(f"Permission to land received - {str(msg.sender)}")
                response = Message(to=str(msg.sender))
                response.body = "Permission to land granted"
                await self.send(response)
                
            elif msg.body == "Permission to land?" and self.agent.get("landingTrack").get_available() == False:
                print(f"Permission to land received - {str(msg.sender)}")
                response = Message(to=str(msg.sender))
                response.body = "Permission to land denied"
                await self.send(response)
        # else:
        #     # No response received within timeout period
        #     self.agent.timeout()
