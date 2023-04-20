from spade.agent import Agent

class Control_Tower(Agent):
    
    async def setup(self):
        print(f"Control Tower {str(self.jid)}" + " starting...")