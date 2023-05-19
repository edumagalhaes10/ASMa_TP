from spade.behaviour import CyclicBehaviour
from spade.message import Message

class HangarManagerListener(CyclicBehaviour):
    async def run(self):
        msg = await self.receive()
        if msg:
            performative = msg.get_metadata('performative')
            if performative == "request":
                body = msg.body.split(" > ")
                if body[0].strip() == "Is there any free hangar?":
                    id = body[1].strip()
                    type = body[2].strip()
                    tracks = body[3].strip()
                    tracks = tracks.split(" | ")

                    treated_tracks = {}
                    for t in tracks:
                        aux = t.split(": ")
                        id_track = aux[0]
                        xy = aux[1].split(",") 
                        treated_tracks[id_track] = xy

                  
                    id_track, available = self.agent.closest_available(type, id, treated_tracks)
                    if available == None:
                        available = "There is no free hangar, added to a queue." + " > " + id
                    else:
                        available = str(available) + " > " + id_track + " > " + id + " > " + type 


                    response = Message(to=str(msg.sender))
                    response.body = available
                    response.set_metadata("performative", "confirm")
                    await self.send(response)
                
                elif body[0].strip() == "Add to an hangar":

                    id = body[1].strip()
                    type = body[2].strip()
                    hangar = self.agent.add_plane_to_hangar(type, id)
                    response = Message(to=str(msg.sender))
                    response.body = f"Initial Hangar > {hangar} > {id}"
                    response.set_metadata("performative", "confirm")
                    await self.send(response)



            elif performative == "inform":
                # print("REMOVE PLANE FROM HANGAR")
                body = msg.body.split(" > ")
                id = body[0].strip()
                self.agent.remove_plane_from_hangar(id)






                


            

   