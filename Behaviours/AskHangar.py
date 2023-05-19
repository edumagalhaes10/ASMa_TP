from spade.behaviour import OneShotBehaviour
from spade.message import Message

class AskHangar(OneShotBehaviour):
    # f'''Plane: {self.get("id")} | Jid: {self.get("jid")} | Type: {self.get("Type")} | Company: {self.get("Company")} | Origin: {self.get("Origin")} | Destination: {self.get("Destination")} | Fuel: {self.get("Fuel")} | Status: {self.get("status")}'''

    def __init__(self, plane, list_tracks):
        self.plane = plane
        self.list_tracks = ""
        for i,tr in enumerate(list_tracks):
            self.list_tracks += f"{tr[0]}: {tr[1][0]},{tr[1][1]}"
            if i != len(list_tracks) - 1:
                self.list_tracks += f" | "

        super().__init__()

    async def run(self):
        msg = Message(to=self.agent.get("hangar_manager"))
        msg.body = f"Is there any free hangar? > {self.plane.get_jid()} > {self.plane.get_type()} > {self.list_tracks}"
        msg.set_metadata("performative", "request")
        await self.send(msg)

