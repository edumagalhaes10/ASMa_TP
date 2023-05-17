from spade.agent import Agent
from Behaviours.ConfirmTakeOff import ConfirmTakeOff
from Behaviours.ConfirmLanding import ConfirmLanding
from UtilsAirport.LandingTrack import LandingTrack
from Behaviours.ControlTowerListener import ControlTowerListener


class Control_Tower(Agent):
    
    # MAIN COMMUNICATIONS HISTORY -> GUARDAR
    # Quando incializamos avioes para descolar, mete-los num hangar primeiro -> ACHO Q ESTÁ 
    # VERIFICAR QUE ESTAMOS A ADICIONAR E A REMOVER AVIOES DOS HANGARS

    async def setup(self):
        print(f"Control Tower {str(self.jid)}" + " starting...")
        # JUNTAR 2 QUEUES PARA SER MAIS FACIL A SUA GESTÃO. AVIOES QUE PEDEM PARA ATERRAR DE URGENCIA PASSAM A FRENTE NA FILA 
        self.set("Queue",[])
        # self.set("landingQueue", [])
        # self.set("takeOffQueue",[])
        self.set("planeInOperation", ("",""))
        self.set("maxPlanes2Land", 10)
        landingTrack = LandingTrack(0,0)
        # landingTrack1 = LandingTrack(100,100)
        # landingTrack2 = LandingTrack(-100,-100)

        # self.set("landingTrack", landingTrack)
        self.set("landingTrack", landingTrack)
        self.set("CommercialHangarsOccupied", 0)
        self.set("CargoHangarsOccupied", 0)

        #SECALHAR JUNTAR ESTES DOIS BEHAVIOURS
        c = ControlTowerListener()
        c = self.add_behaviour(c)
        a = ConfirmTakeOff()  
        self.add_behaviour(a)
        b = ConfirmLanding()
        self.add_behaviour(b)
