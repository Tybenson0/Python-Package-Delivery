from StatusEnum import DeliveryStatus
# Create class for packages
class CreatePackage:
    def __init__(self, ID, address, city, state, zipcode, Deadline_time, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.Deadline_time = Deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        self.truck = None
        
    # returns values as strings
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zipcode,
                                                       self.Deadline_time, self.weight, self.delivery_time,
                                                       self.status, "This package is on truck: ", self.truck)

        # updates status if departure time depending on the time passed in. 
        # ex. if the delivery time is less than the current time we know it has been delivered
    def update_status(self, convert_timedelta):
        if self.delivery_time < convert_timedelta:
            self.status = DeliveryStatus.DELIVERED.value
            self.truck = None
        elif self.departure_time > convert_timedelta:
            self.status = DeliveryStatus.EN_ROUTE.value
        else:
            self.status = DeliveryStatus.AT_HUB.value
            
    # Updates the packages address with the matching ID according to parameters
    def update_address(self, convert_timedelta, set_time, address, zipCode, id): 
            if convert_timedelta > set_time and self.ID == id:
                self.address = address
                self.zipcode = zipCode
    