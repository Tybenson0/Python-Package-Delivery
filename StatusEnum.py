from enum import Enum
#used for setting the status of each package 
class DeliveryStatus(Enum):
    AT_HUB = "At hub"
    EN_ROUTE = "En route"
    DELIVERED = "Delivered"