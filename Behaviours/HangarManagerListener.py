from spade.behaviour import CyclicBehaviour
from spade.message import Message

class HangarManagerListener(CyclicBehaviour):
    async def run(self):
        # Wait for a message granting or denying permission to take off
        msg = await self.receive()
        if msg:
            performative = msg.get_metadata('performative')
            # Process the response
            if performative == "request":
                # print(msg.body)
                body = msg.body.split("> ")
                id = body[1].strip()
                type = body[2].strip()
                # print(id)
                #MUDAR ISTO PARA RECEBER TAMBEM O TIPO DE HANGAR 
                available = self.agent.closest_available(type, id)
                if available == None:
                    available = "There is no free hangar, added to a queue." + " > " + id
                else:
                    available = str(available) + " > " + id

                # print("AVAILABLE: ",available)

                response = Message(to=str(msg.sender))
                response.body = available
                # N SEI SE PERFORMATIVE ESTA CERTA
                response.set_metadata("performative", "confirm")
                await self.send(response)

            elif performative == "inform":
                body = msg.body.split(" > ")
                id = body[0].strip()
                print("///////////////////BODY:", body)
                # IR BUSCAR TIPO DO AVIAO
                self.agent.add_plane_to_hangar("commercial", id)






                


            

   