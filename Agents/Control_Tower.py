from spade.agent import Agent
from Behaviours.ReceiveTakeOffRequest import ReceiveTakeOffRequest
from Behaviours.ReceiveLandingRequest import ReceiveLandingRequest
from UtilsAirport.LandingTrack import LandingTrack
from Behaviours.ControlTowerListener import ControlTowerListener
import json
import random

class Control_Tower(Agent):

    async def setup(self):
        f = open("conf.json")
        conf = json.load(f)
        print(f"Control Tower {str(self.jid)}" + " starting...")
        self.set("Queue",[])
        self.set("maxPlanes2Land", conf["maxPlanesWaiting2Land"])
        self.set("frozenTracks", [])
        self.set("help_structure", {})
        self.set("Landings", 0)
        self.set("Taking Offs", 0)
        self.set("Canceled Landings", 0)



        array_landing_tracks = []
        for index in range(conf["nr_tracks"]):
            x = "%.2f" % random.uniform(-1000, 1000)
            y = "%.2f" % random.uniform(-1000, 1000)
            landingTrack = LandingTrack(x,y,index)
            array_landing_tracks.append(landingTrack)

        self.set("landingTrack", array_landing_tracks)
        self.set("CommercialHangarsOccupied", 0)
        self.set("CargoHangarsOccupied", 0)

        c = ControlTowerListener()
        c = self.add_behaviour(c)
        a = ReceiveTakeOffRequest()  
        self.add_behaviour(a)
        b = ReceiveLandingRequest()
        self.add_behaviour(b)

    def any_free_track(self):
        ret = []
        ret2 = []
        for track in self.get("landingTrack"):
            if track.get_available() == True:
                ret.append((track.get_id(),track.get_coords()))    
                ret2.append(track.get_id())    
                track.set_available(False)
        self.set("frozenTracks", ret2)

        return ret    
    
    def free_tracks(self, id_track, plane, state):
        if id_track:
            for track in self.get("landingTrack"):

                if track.get_id().strip() != id_track and track.get_id().strip() in self.get("frozenTracks"): 
                    track.set_available(True)
                elif track.get_id() == id_track:
                    plane_info = self.get("help_structure")[plane]
                    track.set_plane(plane_info, state) 
                    self.get("help_structure").pop(plane)
        else:
            for track in self.get("landingTrack"):
                if track.get_id().strip() in self.get("frozenTracks"):
                    track.set_available(True)

        self.set("frozenTracks", [])
    
    def free_used_track(self, id_plane):
        for track in self.get("landingTrack"):
            if isinstance(track.get_plane(), str)  and track.get_plane() == id_plane: 
                    track.set_available(True)
                    track.remove_plane()
            
            elif not isinstance(track.get_plane(), str) and track.get_plane():

                if track.get_plane().get_jid() == id_plane: 
                    track.set_available(True)
                    track.remove_plane()
            

    def choose_track_to_takeOff(self, plane, x, y):
        track_chosen = None
        for track in self.get("landingTrack"):
            if track.get_id() in self.get("frozenTracks"):
                x, y = track.get_coords()
                if track_chosen == None:
                    track_chosen = track 
                elif ( (pow(float(x)- float(track.x),2) + pow(float(y)- float(track.y),2)) < (pow(float(x)- float(track_chosen.x),2) + pow(float(y)- float(track_chosen.y),2))):
                    track_chosen = track


        if track_chosen != None:
            track_chosen.set_plane(plane, "Taking Off")

            for track in self.get("landingTrack"):
                if track.get_id() in self.get("frozenTracks") and track.get_id()!=track_chosen.get_id():
                    track.set_available(True)
            
            self.set("frozenTracks", [])



        return track_chosen


    def count_planes_waiting2land(self):
        count = 0
        for plane in self.get("Queue"):
            if plane[1] == "Waiting To Land":
                count += 1
        return count
    
    def results(self):
        with open("results.json", "w") as outfile:
            dictionary = {}
            dictionary["Landings"] = self.get("Landings")
            dictionary["Taking Offs"] = self.get("Taking Offs")
            dictionary["Canceled Landings"] = self.get("Canceled Landings")
            json.dump(dictionary, outfile)
            outfile.flush()