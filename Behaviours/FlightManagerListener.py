from spade.behaviour import CyclicBehaviour
from spade.message import Message
from termcolor import colored
import os


class FlightManagerListener(CyclicBehaviour):

    async def on_start(self):
        self.counter = 0

    async def run(self):
        # Wait for a message granting or denying permission to take off
        msg = await self.receive()
        if msg:
            performative = msg.get_metadata('performative')
            # Process the response
            if performative == "inform":
                
                color = "yellow"

                # os.system('clear')
                print(colored("*"*188, color))
                
                body = msg.body.split(" \n ")
                for b in body:
                    b = b.split("> ")


                    if b[0] == "Plane In Operation":
                        new_b = b[1].split(" $ ")
                        print(colored(b[0]+": \n", color, attrs=["bold"]))
                        if b[1]:
                            for item in new_b:
                                print(item)
                        else: print("    Empty\n")
                    elif b[0] == "Airport Queue":
                        new_b = b[1].split(" $ ")
                        print(colored(b[0]+": \n", color, attrs=["bold"]))
                        if b[1]:
                            for item in new_b:
                                print(item)
                        else: print("    Empty\n")
                    else:
                        print(colored(b[0]+": ", color, attrs=["bold"]) + " " + b[1] + "\n")

                # print(msg.body)


                print(colored("*"*188, color))
                self.counter +=1

                


            

   