import getpass
import time
import json
import webbrowser

from spade import quit_spade
from Agents.Plane import Plane
from Agents. Control_Tower import Control_Tower
from Agents.Hangar_Manager import Hangar_Manager
from Agents.Flight_Manager import Flight_Manager


#Import Agents

if __name__ == "__main__":
    # ,f'plane{i}',"Ryanair", "Passengers", "Porto", "Lisboa", "TakingOff"
    
    default_info = {"company":"Ryanair", "type":"Passengers", "origin":"Porto", "destination":"Lisboa"}

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
    control_tower.web.start(hostname="127.0.0.1", port="10000")
    webbrowser.open("127.0.0.1:10000/spade")

    hangar_manager_jid = "hangar_manager" + jid
    hangar_manager = Hangar_Manager(hangar_manager_jid, pwd)
    hangar_manager.set("jid", hangar_manager_jid)
    hangar_manager.set("control_tower", control_tower_jid)
    hangar_manager.start()

    flight_manager_jid = "flight_manager" + jid
    flight_manager = Flight_Manager(flight_manager_jid, pwd)
    flight_manager.set("jid", flight_manager_jid)
    flight_manager.set("control_tower", control_tower_jid)
    flight_manager.start()
    # flight_manager.web.start(hostname="127.0.0.1", port="10001")

    # time.sleep(5)

    planes = {}
    print("Creating 4 Planes...")
    for i in range(4):
        plane_jid = f'plane{i}{jid}'
        plane = Plane(plane_jid,pwd)
        plane.set('jid', plane_jid) 
        plane.set('id', f'plane{i}')
        for key, value in default_info.items():
            plane.set(key, value)
        if i<2:
            # print("JID: ",plane.get('jid'))
            # print("Company: ",plane.get('company'))
            plane.set("status", "permission2TakeOff")
        else:
            plane.set("status", "permission2Land")
        
        
        plane.set("control_tower", control_tower_jid)
        planes[f'plane{i}'] = plane
        plane.start()
        plane.web.start(hostname="127.0.0.1", port=f"1000{i+1}")

    # for p in planes.values():
    #     print(p.__str__())


    # print([p.__str__ for p in planes.values()])
    while control_tower.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for id, p in planes.items():
                print(id)
                p.stop()
            flight_manager.stop()
            hangar_manager.stop()
            control_tower.stop()
            break
    print("Agents finished")
    quit_spade()