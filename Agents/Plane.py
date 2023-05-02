from spade.agent import Agent
from Behaviours.Permission2TakeOff import Permission2TakeOff
from Behaviours.PlaneListener import PlaneListener
from Behaviours.Permission2Land import Permission2Land
from Behaviours.LandingTakeOffDone import LandingTakeOffDone


class Plane(Agent):

    def __str__(self):
        return f'''*****
PLANE {self.get("id")}
JID: {self.get("jid")}
COMPANY: {self.get("company")}
*****'''

    async def setup(self):
        print(f"Plane {str(self.jid)}" + " starting...")

        if self.get("status") == "permission2TakeOff":
            a = Permission2TakeOff()
            self.add_behaviour(a)
        elif self.get("status") == "permission2Land":
            a = Permission2Land()
            self.add_behaviour(a)

        b = PlaneListener()
        self.add_behaviour(b)

        # c = LandingTakeOffDone()
        # self.add_behaviour(c)
