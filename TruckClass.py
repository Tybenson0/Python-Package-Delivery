# Truck class that creates truck objects, and initializes some of the constant data
class CreateTruck:
    def __init__(self, packages, departTime):
        self.capacity = 16
        self.speed = 18
        self.load = None
        self.packages = packages
        self.mileage = 0.0
        self.address = "4001 South 700 East"
        self.depart_time = departTime
        self.time = departTime
        self.hasDriver = False
    
    #returns values as strings
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.capacity, self.speed, self.load, self.packages, self.mileage,
                                               self.address, self.depart_time)
