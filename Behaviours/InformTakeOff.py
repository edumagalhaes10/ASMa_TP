from spade.behaviour import OneShotBehaviour
from spade.message import Message

class InformTakeOff(OneShotBehaviour):
    async def run(self):
        msg = Message(to=str(self.agent.get("planeInOperation")[0].get_jid()))
        msg.body = "Permission to take off granted"
        msg.set_metadata("performative", "inform") # N sei se está bem

        clear_hangar = Message(to=self.agent.get("hangar_manager"))
        plane = str(self.agent.get("planeInOperation")[0].get_jid())
        clear_hangar.body = f"{plane} > Leaving Hangar"
        clear_hangar.set_metadata("performative", "inform")
        # PERFORMATIVE
        await self.send(msg)

