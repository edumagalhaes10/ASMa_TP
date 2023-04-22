from spade.behaviour import CyclicBehaviour
from spade.message import Message

class PlaneListener(CyclicBehaviour):
    async def run(self):
        response = await self.receive()
        if response:
            print("RESPONSE: ",response.body)
            if response.body == "Permission to take off granted":
                print("Almost Taking Off")
            elif response.body == "Permission to take off denied":
                print("Permission to take off denied")

            if response.body == "Permission to land granted":
                print("Almost Landing")
            elif response.body == "Permission to land denied":
                print("Permission to land denied")
