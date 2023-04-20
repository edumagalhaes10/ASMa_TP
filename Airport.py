import getpass
import time
import json

from spade import quit_spade
from Agents.Plane import Plane
from Agents. Control_Tower import Control_Tower
from Agents.Hangar_Manager import Hangar_Manager
from Agents.Flight_Manager import Flight_Manager


#Import Agents

if __name__ == "__main__":
    # ,f'plane{i}',"Ryanair", "Passengers", "Porto", "Lisboa", "TakingOff"
    
    default_info = {"company":"Ryanair", "type":"Passengers", "origin":"Porto", "destination":"Lisboa", "status":"TakingOff"}

    f = open("conf.json")
    conf = json.load(f)
    pwd = conf["pwd"]
    jid = conf["jid"]
    
    #Create and start Agents
    control_tower_jid = "control_tower" + jid
    control_tower = Control_Tower(control_tower_jid, pwd)
    control_tower.set("jid", control_tower_jid)
    print("Control Tower JID: ",control_tower.get("jid"))
    res_control_tower = control_tower.start()
    res_control_tower.result()

    planes = {}
    print("Creating 4 Planes...")
    for i in range(4):
        if i<2:
            plane_jid = f'plane{i}{jid}'
            plane = Plane(plane_jid,pwd)
            plane.set('jid', plane_jid) 
            plane.set('id', f'plane{i}')
            for key, value in default_info.items():
                plane.set(key, value)
            # print("JID: ",plane.get('jid'))
            # print("Company: ",plane.get('company'))
            planes[f'plane{i}'] = plane
        else:
            pass

        plane.start()

    for p in planes.values():
        print(p.__str__())


    # print([p.__str__ for p in planes.values()])
    while control_tower.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for id, p in planes.items():
                print(id)
                p.stop()
            control_tower.stop()
            break
    print("Agents finished")
    quit_spade()