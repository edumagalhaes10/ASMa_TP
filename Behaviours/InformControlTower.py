from spade.behaviour import OneShotBehaviour
from spade.message import Message

class InformControlTower(OneShotBehaviour):
    async def run(self):
        print("Inform Control Tower")
        msg = Message(to=self.agent.get("control_tower"))
        msg.body = f"Hangars Info\n Comercial hangars: {self.agent.get('comercial_hangars')} | Cargo hangars: {self.agent.get('cargo_hangars')}"
        msg.set_metadata("performative", "inform")
        await self.send(msg)

