from spade.agent import Agent

class Plane(Agent):

    def __str__(self):
        return f'''*****
PLANE {self.get("id")}
JID: {self.get("jid")}
COMPANY: {self.get("company")}
*****'''

    async def setup(self):
        print(f"Plane {str(self.jid)}" + " starting...")


        #Add Behaviours
        # a = Behaviour X
        # b = Behaviour Y
        # self.add_behaviour(a)
        # self.add_behaviour(b)
