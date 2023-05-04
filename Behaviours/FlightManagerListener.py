from spade.behaviour import CyclicBehaviour
from spade.message import Message

class FlightManagerListener(CyclicBehaviour):
    async def run(self):
        # Wait for a message granting or denying permission to take off
        msg = await self.receive()
        if msg:
            performative = msg.get_metadata('performative')
            # Process the response
            if performative == "inform":
                print(msg.body)

                


            

   