
class PlaneInfo:


    def __init__(self, array_info): #, id, jid, type,company, origin, destination, fuel, status):
        self.id = array_info[0]
        self.jid = array_info[1]
        self.type = array_info[2]
        self.company = array_info[3]
        self.origin = array_info[4]
        self.destination = array_info[5]
        self.fuel = array_info[6]
        self.status = array_info[7]

    def get_id(self):
        return self.id
    
    def get_type(self):
        return self.type
    
    def get_jid(self):
        return self.jid
    
    def get_company(self):
        return self.company
    
    def get_origin(self):
        return self.origin
    
    def get_destination(self):
        return self.destination
    
    def get_fuel(self):
        return self.fuel
    
    def get_status(self):
        return self.status

    def __str__(self):
        return f'''Plane: {self.get_id()} | Jid: {self.get_jid()} | Type: {self.get_type()} | Company: {self.get_company()} | Origin: {self.get_origin()} | Destination: {self.get_destination()} | Fuel: {self.get_fuel()}'''

