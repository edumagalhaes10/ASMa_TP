from spade.behaviour import CyclicBehaviour
from spade.message import Message

class ConfirmTakeOff(CyclicBehaviour):
    async def run(self):
        # Wait for a message granting or denying permission to take off
        msg = await self.receive()
        if msg:
            # Process the response
            if msg.body == "Permission to take off?":
                print(f"Permission to take off received - {str(msg.sender)}")
                response = Message(to=str(msg.sender))
                response.body = "Permission to take off granted"
                await self.send(response)
            # else:
            #     self.agent.deny_takeoff()
        # else:
        #     # No response received within timeout period
        #     self.agent.timeout()