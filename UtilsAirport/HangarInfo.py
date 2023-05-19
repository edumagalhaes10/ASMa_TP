class HangarInfo:
    def __init__(self, hangar_array):
        self.hangar_id = hangar_array[0]
        self.x = hangar_array[1]
        self.y = hangar_array[2]
        
    def get_coords(self):
        return self.x, self.y

    def get_id(self):
        return self.hangar_id
    
    def __str__(self):
        return f'''Hangar Id: {self.hangar_id} | X: {self.x} | Y: {self.y}'''
