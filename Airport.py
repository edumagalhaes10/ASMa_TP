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
from Behaviours.Add2RandomHangar import Add2RandomHangar



#Import Agents

# SECALHAR MUDAR SET DO TIPO PARA AQUI PARA SER MAIS FACIL COMPARAR COM NR MAXIMO DE HANGARS NO INICIO CASO SEJA TAKE OFF...  FALTA VERIFICAR SE EXCEDE NUMERO DE HANGARES DISPONIVEIS

# FUEL PARA PASSAR A FRENTE NA FILA -> NEGOCIAÇAO COM A TORRE DE CONTROLO PARA PASSAR A FRENTE NA FILA

# BLACKBOX NOS AVIOES PARA SALVAGUARDAR AS COMUNICAÇOES...
# LOGS EM CADA AGENTE...
# ISTO SE HOUVER TEMPO !!!!!!!!!!



#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# DECREMENTO DO NUMERO DE HANGARS OCUPADOS IS NOT OK -> ACHO Q JÁ ESTÁ CHECK !!!!!
# ADICIONAR TIPO DO AVIAO A TODAS AS OPERACOES -> É IMPORTANTE SENAO ESTA SEMPRE A ADICIONAR E TIRAR DOS HANGARES COMERCIAIS -> ACHO Q JÁ ESTÁ CHECK !!!!! 

# QUANDO AVIAO DESCOLA, AS VEZES BUGA E N RETIRA DO HANGAR... N SEI PQ, VERIFICAR ISTO -> ACHO Q JÁ ESTÁ CHECK !!!!! 

# MATAR AGENTES DEPOIS DE DESCOLAR... CHECK

# FALTA TIMER PARA AVIOES IREM EMBORA CASO N POSSAM ATERRAR PASSADO X TEMPO -> CHECK
# FALTA REMOVER O TIMEOUT BEHAVIOUR DOS AGENTES Q SAO ACEITES PARA ATERRAR...  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CHECK

# Tempo de circulaçao, pidsta, descolagem tudo junto num timeout behaviour... PERGUNTAR -> CHECK -> FALAR NO RELATORIO SOBRE A DECISÃO

class Airport:
    def run_airport(self):
        f = open("conf.json")
        conf = json.load(f)

        if conf["nr_takeoff"] > conf["Commercial_hangars"] + conf["Cargo_hangars"]:
            print(colored("Conf file is not well defined. Initial Planes that want to Take Off must be lesser or equal than the sum of Commercial and Cargo Hangars.", "red"))
        else:
            text = colored(pyfiglet.figlet_format("AIRPORT", font = "slant"), "yellow")
            print(text)


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
            try:
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
                # wait a bit to start all of the previous agents
                time.sleep(10)

                planes = {}
                print("Creating 4 Planes...")      
                nr_landing = conf["nr_landing"]
                nr_takeoff = conf["nr_takeoff"]
                nr_planes = nr_landing+nr_takeoff

                for i in range(nr_planes):
                    time.sleep(1)
                    last = 0
                    plane_jid = f'plane{i}{jid}'
                    plane = Plane(plane_jid,pwd)
                    plane.set('jid', plane_jid) 
                    plane.set('id', f'plane{i}')
                    plane.set("control_tower", control_tower_jid)
                    if i<nr_takeoff:
                        plane.set("status", "permission2TakeOff")
                    else:
                        plane.set("status", "permission2Land")

                    planes[f'plane{i}'] = plane
                    plane.start()
                    if plane.get("status") == "permission2TakeOff":
                        while plane.get("Type") == None:
                            time.sleep(1)
                        type = plane.get("Type")
                        print("TYPE PLANE: ", type)
                        if type == "Commercial":
                            if control_tower.get("CommercialHangarsOccupied") == control_tower.get("Commercial hangars"):
                                plane.set("Type", "Cargo")
                                last = control_tower.get("CargoHangarsOccupied")
                                control_tower.set("CargoHangarsOccupied", last + 1)
                                # print("CONTROL TOWER CARGO ", control_tower.get("CargoHangarsOccupied"))
                            else:    
                                last = control_tower.get("CommercialHangarsOccupied")
                                control_tower.set("CommercialHangarsOccupied", last + 1)
                                # print("CONTROL TOWER COMMERCIAL ", control_tower.get("CommercialHangarsOccupied"))
                        else:
                            if control_tower.get("CargoHangarsOccupied") == control_tower.get("Cargo hangars"):
                                plane.set("Type", "Cargo")
                                last = control_tower.get("CommercialHangarsOccupied")
                                control_tower.set("CommercialHangarsOccupied", last + 1)
                                # print("CONTROL TOWER CARGO ", control_tower.get("CommercialHangarsOccupied"))
                            else:
                                last = control_tower.get("CargoHangarsOccupied")
                                control_tower.set("CargoHangarsOccupied", last + 1)
                                # print("CONTROL TOWER CARGO ", control_tower.get("CargoHangarsOccupied"))

                        add2randomhangar = Add2RandomHangar(plane.get("jid"), plane.get("Type"))
                        plane.add_behaviour(add2randomhangar)

                    plane.web.start(hostname="127.0.0.1", port=f"1000{i}")

                index = nr_planes + 1
                time.sleep(10)

                # for p in planes.values():
                #     print(p.__str__())
                while control_tower.is_alive():
                    time.sleep(2)
                    last = 0
                    plane_jid = f'plane{index}{jid}'
                    plane = Plane(plane_jid,pwd)
                    plane.set('jid', plane_jid) 
                    plane.set('id', f'plane{index}')
                    plane.set("status", "permission2Land")
                    plane.set("control_tower", control_tower_jid)
                    planes[f'plane{index}'] = plane
                    plane.start()
                    plane.web.start(hostname="127.0.0.1", port=f"1000{index}") 
                    index+=1
            except KeyboardInterrupt:
                for id, p in planes.items():
                    print(id)
                    p.stop()
                flight_manager.stop()
                hangar_manager.stop()
                control_tower.results()
                control_tower.stop()
                print("Agents finished")
                quit_spade()


if __name__ == "__main__":
    airport = Airport()
    airport.run_airport()