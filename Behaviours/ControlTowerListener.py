from spade.behaviour import CyclicBehaviour
from spade.message import Message
import re

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

                elif msg.body=="Landing Completed":
                    print("RECEIVED - ",str(msg.body))
                    self.agent.set("planeInOperation",("",""))
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
                


            

   