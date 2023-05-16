import time
import json
import webbrowser
import pyfiglet
from termcolor import colored

from spade import quit_spade
from Agents.Plane import Plane
from Agents. Control_Tower import Control_Tower
from Agents.Hangar_Manager import Hangar_Manager
from Agents.Flight_Manager import Flight_Manager


#Import Agents

#SECLAHAR MUDAR SET DO TIPO PARA AQUI PARA SER MAIS FACIL COMPARAR COM NR MAXIMO DE HANGARS NO INICIO CASO SEJA TAKE OFF... 
#FALTA TIMER PARA AVIOES IREM EMBORA CASO N POSSAM ATERRAR PASSADO X TEMPO
#FUEL PARA PASSAR A FRENTE NA FILA

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# DECREMENTO DO NUMERO DE HANGARS OCUPADOS IS NOT OK -> ACHO Q JÁ ESTÁ CHECK !!!!!
#ADICIONAR TIPO DO AVIAO A TODAS AS OPERACOES -> É IMPORTANTE SENAO ESTA SEMPRE A ADICIONAR E TIRAR DOS HANGARES COMERCIAIS -> ACHO Q JÁ ESTÁ CHECK !!!!! 

# QUANDO AVIAO DESCOLA, AS VEZES BUGA E N RETIRA DO HANGAR... N SEI PQ, VERIFICAR ISTO -> ACHO Q JÁ ESTÁ CHECK !!!!! 


if __name__ == "__main__":
    # ,f'plane{i}',"Ryanair", "Passengers", "Porto", "Lisboa", "TakingOff"
    
    text = colored(pyfiglet.figlet_format("AIRPORT", font = "slant"), "yellow")
    print(text)

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
    control_tower.web.start(hostname="127.0.0.1", port="8080")
    # webbrowser.open("127.0.0.1:8080/spade")

    hangar_manager_jid = "hangar_manager" + jid
    hangar_manager = Hangar_Manager(hangar_manager_jid, pwd)
    hangar_manager.set("jid", hangar_manager_jid)
    hangar_manager.set("control_tower", control_tower_jid)
    hangar_manager.web.start(hostname="127.0.0.1", port="8081")

    control_tower.set("hangar_manager", hangar_manager_jid)

    hangar_manager.start()

    flight_manager_jid = "flight_manager" + jid
    flight_manager = Flight_Manager(flight_manager_jid, pwd)
    flight_manager.set("jid", flight_manager_jid)
    flight_manager.set("control_tower", control_tower_jid)
    control_tower.set("flight_manager", flight_manager_jid)

    flight_manager.start()
    flight_manager.web.start(hostname="127.0.0.1", port="8082")
    # await my_agent.start()
    # wait a bit to start all of the previous agents
    time.sleep(10)

    planes = {}
    print("Creating 4 Planes...")      
    # When creating take off planes, must add them to hangar...
    for i in range(5):
        last = 0
        plane_jid = f'plane{i}{jid}'
        plane = Plane(plane_jid,pwd)
        plane.set('jid', plane_jid) 
        plane.set('id', f'plane{i}')
        # for key, value in default_info.items():
        #     plane.set(key, value)
        if i<3:
            # print("JID: ",plane.get('jid'))
            # print("Company: ",plane.get('company'))
            # plane.set("status", "permission2TakeOff")

            plane.set("status", "permission2Land")

        else:
            plane.set("status", "permission2TakeOff")

            # plane.set("status", "permission2Land")

        plane.set("control_tower", control_tower_jid)
        planes[f'plane{i}'] = plane
        plane.start()
        if plane.get("status") == "permission2TakeOff":
            while plane.get("Type") == None:
                time.sleep(1)
            type = plane.get("Type")
            print("TYPE PLANE: ", type)
            if type == "Commercial":
                last = control_tower.get("CommercialHangarsOccupied")
                control_tower.set("CommercialHangarsOccupied", last + 1)
            else:
                last = control_tower.get("CargoHangarsOccupied")
                # print("!!!!!!!!!!!!!!    LAST CARGO NR = ", last)
                control_tower.set("CargoHangarsOccupied", last + 1)

        plane.web.start(hostname="127.0.0.1", port=f"1000{i+1}")

    time.sleep(10)

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
            flight_manager.stop()
            hangar_manager.stop()
            control_tower.stop()
            break
    print("Agents finished")
    quit_spade()