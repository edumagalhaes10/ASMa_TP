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
        self.set("Queue",[])
        self.set("planeInOperation", ("",""))
        self.set("new_planesInOperation", [])
        self.set("maxPlanes2Land", 10)
        self.set("frozenTracks", [])
        index = 0
        landingTrack = LandingTrack(0,0,index)

        index += 1
        landingTrack1 = LandingTrack(100,100,index)

        index +=1
        landingTrack2 = LandingTrack(-100,-100,index)

        index += 1
        landingTrack3 = LandingTrack(-500,-200,index)

        #...

        self.set("landingTrack", [landingTrack, landingTrack1, landingTrack2,landingTrack3])
        self.set("CommercialHangarsOccupied", 0)
        self.set("CargoHangarsOccupied", 0)

        #SECALHAR JUNTAR ESTES DOIS BEHAVIOURS
        c = ControlTowerListener()
        c = self.add_behaviour(c)
        a = ConfirmTakeOff()  
        self.add_behaviour(a)
        b = ConfirmLanding()
        self.add_behaviour(b)

    # def any_free_track(self):
    #     ret = False
    #     for track in self.get("landingTrack"):
    #         if track.get_available() == True:
    #             ret = True
    #             track.set_available(False)
        
    #     return ret
    
    def any_free_track(self):
        ret = []
        ret2 = []
        for track in self.get("landingTrack"):
            # print("TRACK AVAILABLE: ", track.get_available())
            if track.get_available() == True:
                ret.append((track.get_id(),track.get_coords()))    
                ret2.append(track.get_id())    
                track.set_available(False)
        self.set("frozenTracks", ret2)
        # print("FROZEN TRACKS: ", ret2)

        return ret    
    
    def free_tracks(self, id_track, plane, state):
        print("MAN, ENTREI NA CENA DE DAR FREE DAS TRACKS")
        if id_track:
            for track in self.get("landingTrack"):
                # print("+++\n",track.get_id().strip(), " | id:track:", id_track.strip(), "\n +++")
                # print("+++\n", self.get("frozenTracks"), "\n +++")
                if track.get_id().strip() != id_track and track.get_id().strip() in self.get("frozenTracks"): 
                    track.set_available(True)
                    # print("MAN, MUDEI O ESTADO PARA TRUE")
                elif track.get_id() == id_track:
                    track.set_plane(plane, state) 
                    # print("MAN, ADICIONEI O PLANE")
        else:
            for track in self.get("landingTrack"):
                if track.get_id().strip() in self.get("frozenTracks"):
                    track.set_available(True)

        self.set("frozenTracks", [])
    
    def free_used_track(self, id_plane):
        # print("ID_PLANE: ", id_plane)
        for track in self.get("landingTrack"):
            plane = track.get_plane()
            # print("+++\n",plane, " | id:plane:", id_plane, "\n +++")

            # print("ID_PLANE_TRACK: ", track.get_plane())
            if isinstance(track.get_plane(), str)  and track.get_plane() == id_plane: 
                    track.set_available(True)
                    track.remove_plane()
            
            elif not isinstance(track.get_plane(), str) and track.get_plane():

                if track.get_plane().get_jid() == id_plane: 
                    track.set_available(True)
                    track.remove_plane()
            

    def choose_track_to_takeOff(self, plane, x, y):
        track_chosen = None
        # print("PLANEEEEEEE ID", plane.get_id())
        for track in self.get("landingTrack"):
            if track.get_id() in self.get("frozenTracks"):
                x, y = track.get_coords()
                if track_chosen == None:
                    track_chosen = track 
                elif ( (pow(float(y)- float(track.x),2) + pow(float(y)- float(track.y),2)) < (pow(float(x)- float(track_chosen.x),2) + pow(int(y)- float(track_chosen.y),2))):
                    track_chosen = track


        if track_chosen != None:
            track_chosen.set_plane(plane, "Taking Off")

            for track in self.get("landingTrack"):
                if track.get_id() in self.get("frozenTracks") and track.get_id()!=track_chosen.get_id():
                    track.set_available(True)
            
            self.set("frozenTracks", [])



        return track_chosen

