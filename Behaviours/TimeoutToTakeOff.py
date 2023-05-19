from spade.behaviour import TimeoutBehaviour
from spade.message import Message
from Behaviours.Permission2TakeOff import Permission2TakeOff

class TimeoutToTakeOff(TimeoutBehaviour):

    async def run(self):
        permission2TakeOff = Permission2TakeOff()
        self.agent.add_behaviour(permission2TakeOff)