from spade.agent import Agent
from Behaviours.Permission2TakeOff import Permission2TakeOff
from Behaviours.PlaneListener import PlaneListener
from Behaviours.Permission2Land import Permission2Land

import random

class Plane(Agent):

    def __str__(self):
        return f'''Plane: {self.get("id")} | Jid: {self.get("jid")} | Type: {self.get("Type")} | Company: {self.get("Company")} | Origin: {self.get("Origin")} | Destination: {self.get("Destination")} | Fuel: {self.get("Fuel")} | Status: {self.get("status")}'''

    async def setup(self):
        self.set("flag", True)
        companies = {1:"TAP", 2:"Ryanair", 3:"Aegean Airlines", 4:"AirBaltic", 5:"Air Europa", 6:"Air Transat", 7:"Azores Airlines", 8:"British Airways", 9:"Brussels Airlines", 10:"EasyJet", 11: "Eurowings", 12:"Finnair", 13:"Iberia", 14:"Lufthansa", 15:"Luxair", 16:"Transavia", 17:"Vueling", 18:"Wizz Air", 19:"KLM", 20:"Swiss International"}
        cities = {1:"Viena", 2:"Madrid", 3:"Barcelona", 4:"Paris", 5:"Milão", 6:"Roma", 7:"Budapeste", 8:"Istambul", 9:"Londres", 10:"São Miguel", 11:"Funchal", 12:"Lisboa", 13:"Amsterdão"} # adicionar alguns destinos
        types = {1:"Commercial", 2:"Cargo"}

        print(f"Plane {str(self.jid)}" + " starting...")
        company = companies[random.randint(1, 20)]
        self.set("Company", company)
        self.set("Fuel", random.randint(0, 100))
        self.set("Type",types[random.choices([1,2], [2,1])[0]])
        self.set("Hangar", None)
        self.set("Track", None)


        if self.get("status") == "permission2TakeOff":
            self.set("Destination", cities[random.randint(1, 13)])
            self.set("Origin", "Porto")

        elif self.get("status") == "permission2Land":
            self.set("Destination", "Porto")
            self.set("Origin", cities[random.randint(1, 13)])

            permission2Land = Permission2Land()
            self.add_behaviour(permission2Land )

        b = PlaneListener()
        self.add_behaviour(b)

