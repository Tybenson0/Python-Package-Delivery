# Tyler Benson
# Student ID: 011647231
# The WGU Parcel Service!
import csv
import datetime
import TruckClass
from PackageClass import CreatePackage
from HashClass import CreateHashMap
from StatusEnum import DeliveryStatus

# Reads PackageInfo CSV file
with open("Resources/PackagesInfo.csv") as csvfileforpackageinfo:
    CSV_Packages = csv.reader(csvfileforpackageinfo)
    CSV_Packages = list(CSV_Packages)
# Reads Addresses CSV file
with open("Resources/Addresses.csv") as csvfileforaddresses:
    CSV_Addresses = csv.reader(csvfileforaddresses)
    CSV_Addresses = list(CSV_Addresses)
# Reads Resources CSV file
with open("Resources/Distances.csv") as csvfilefordistances:
    CSV_Distances = csv.reader(csvfilefordistances)
    CSV_Distances = list(CSV_Distances)

# Loops through PackagesInfo CSV file and builds package objects and inserts them into the hash table package_table
def LoadPackages(filename, package_table):
    truck1_packages = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
    truck2_packages = [3, 9, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38]
    truck3_packages = [2, 4, 5, 6, 7, 8, 10, 11, 25, 28, 32, 33, 39]
    with open(filename) as all_package_info:
        current_package_data = csv.reader(all_package_info)
        for package in current_package_data:
            currentPackage = CreatePackage(int(package[0]), package[1], package[2], package[3], package[4], package[5], package[6], DeliveryStatus.AT_HUB.value)
            #assigns each package a truck since it needs to be displayed. 
            if currentPackage.ID in truck1_packages:
                currentPackage.truck = "Truck 1"
            elif currentPackage.ID in truck2_packages:
                currentPackage.truck = "Truck 2"
            elif currentPackage.ID in truck3_packages:
                currentPackage.truck = "Truck 3"
            
            package_table.insert(int(package[0]), currentPackage)

# Function that passes in address string, finds the corresponding string in the Addresses CSV file and returns the location as an integer
def GetAddress(address):
    for row in CSV_Addresses:
        if address in row[2]:
            return int(row[0])

# Function that finds the distance between two addresses
def DistanceBetween(x, y):
    distance = CSV_Distances[x][y]
    if distance == '':
        distance = CSV_Distances[y][x]

    return float(distance)

'''Function that orders packages on the truck and then calculates the distances of each package, checking which
one has the shortest distance between the truck's current position and chooses that location, deliveres the package,
and continues this process until no packages are left.'''
def ShipOut(truck, Hashed_Packages):
    # Takes the truck's packages array and passes each int into the lookup funtion to get the packages from the hash table
    
    PackageInventory = []
    for packageID in truck.packages:
        package = Hashed_Packages.lookup(packageID)
        PackageInventory.append(package)
    # Clears the truck's packages so they can be placed back according to the shortest distances
    truck.packages.clear()
   # Checks that the truck still has packages to be delivered and adds the nearest package each time
    while len(PackageInventory) > 0:
        next_address = 2000
        next_package = None
        for package in PackageInventory:
            if DistanceBetween(GetAddress(truck.address), GetAddress(package.address)) <= next_address:
                next_address = DistanceBetween(GetAddress(truck.address), GetAddress(package.address))
                next_package = package
        # Adds closest package to the truck package list then removes it from the inventory
        truck.packages.append(next_package.ID)
        PackageInventory.remove(next_package)
        # Adds the distance to the total mileage of the truck to keep track of mileage and then updates the truck's current address
        truck.mileage += next_address
        truck.address = next_package.address
        # Updates time according to the distance and the truck's speed
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time
        
    
        
      

class Main:
    print("")
    print("")
    print("-----------------------------------------------------------------------------------")
    print("Welcome to the Western Governor's Univeristy Parcel Service!")
    print("")
    print("Would you like to run the simulation?")
    print("")
    #start of the UI
    
    while True:
        answer = input("Type \"yes\" to start or \"exit\" to close the program: ")
        
        if (answer == "yes"): #Creates trucks, hash table/map, loads the packages and ships out the trucks
            truck_1 = TruckClass.CreateTruck([1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], datetime.timedelta(hours=8))
            # Create truck 2 with it's assigned packages
            truck_2 = TruckClass.CreateTruck([3, 9, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38], datetime.timedelta(hours=10, minutes=20))
            # Create truck 3 with it's assigned packages
            truck_3 = TruckClass.CreateTruck([2, 4, 5, 6, 7, 8, 10, 11, 25, 28, 32, 33, 39], datetime.timedelta(hours=9, minutes=5))
            
             # Create hash table
            Hashed_Packages = CreateHashMap(40)

            # Load packages into hash table
            LoadPackages("Resources/PackagesInfo.csv", Hashed_Packages)
            #Initializes drivers to check if a driver is available
            drivers = 2
            truck_1.hasDriver = True
            drivers = drivers - 1
            truck_2.hasDriver = True
            drivers = drivers - 1
            # Ships out trucks 1 and 2  first since they carry packages with urgent delivery times
            ShipOut(truck_1, Hashed_Packages)
            truck_1.hasDriver = False
            drivers = drivers + 1
            ShipOut(truck_2, Hashed_Packages)
            truck_2.hasDriver = False
            drivers = drivers +1
            # Makes truck 3 wait until one of the trucks is done with it's delivery
            if (drivers != 0):
                truck_3.hasDriver = True
                drivers = drivers - 1
                truck_3.depart_time = min(truck_1.time, truck_2.time)
                ShipOut(truck_3, Hashed_Packages)
            print("")
            print("Simulation ran!")
            print("-----------------------------------------------------------------------------------")
            print("")
            
            break
        elif (answer == "exit"):
            exit()
        else:
            print("")
            print("Not a valid input")
            print("")
    print("")
    print("What would you like to do?")
    print("")
    print("Check total mileage expenditure across trucks?       type \"mileage\"")
    print("")
    print("Check Package Status's at a certain time?            type \"times\"")
    print("")
    print("Type \"Exit\" to exit the program")
    print("")
    while True:
        answer = input("Your choice: ")
        
        if (answer == "mileage"):
            print("")
            print("-----------------------------------------------------------------------------------")
            total_mileage = truck_1.mileage + truck_2.mileage + truck_3.mileage
            print("The total mileage across trucks is: {:.2f}".format(total_mileage)) # Print total mileage for all trucks
            print("-----------------------------------------------------------------------------------")
            print("")
            print("What would you like to do?")
            print("")
            print("Check total mileage expenditure across trucks?       type \"mileage\"")
            print("")
            print("Check Package Status's at a certain time?            type \"times\"")
            print("")
            print("Type \"Exit\" to exit the program")
            print("")
            
        elif(answer == "times"):
                    # The user will be asked to enter a specific time
                    print("-----------------------------------------------------------------------------------")
                    print("")
                    input_time = input("Please enter a time to check status of package's. Use the following format, HH:MM:SS   - ")
                    (h, m, s) = input_time.split(":")
                    print("")
                    convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    # Can display either single package data or all package data at a given time
                    decision_input = input("To view the status of an individual package please type 'single'. For a rundown of all"
                                        " packages please type 'all':  ")
                    print("")
                    # Looks for a single package
                    if decision_input == "single":
                        while(True):
                            try:
                                # Asks user to input the ID for the package
                                ID_input = input("Enter the numeric package ID ")
                                package = Hashed_Packages.lookup(int(ID_input))
                                # Updates status
                                package.update_status(convert_timedelta)
                                # Updates address if the time is after the convert_timedelta
                                package.update_address(convert_timedelta, datetime.timedelta(hours=10, minutes=20, seconds=00), "410 S. State St.", "84111", 9)
                                print("")
                                print("-----------------------------------------------------------------------------------")
                                print(str(package))
                                print("-----------------------------------------------------------------------------------")
                                print("")
                                exit()
                            except ValueError:
                                print("")
                                print("Entry invalid.")
                                print("")
                    # If the user types "all" we display all packages information
                    elif decision_input == "all":
                        while(True):
                            try:
                                print("")
                                print("-----------------------------------------------------------------------------------")
                                for packageID in range(1, 41):
                                    package = Hashed_Packages.lookup(packageID)
                                    package.update_status(convert_timedelta)
                                    # Updates address if the time is after the convert_timedelta
                                    package.update_address(convert_timedelta, datetime.timedelta(hours=10, minutes=20, seconds=00), "410 S. State St.", "84111", 9)
                                    
                                    print(str(package))
                                    print("Package Status at the time of: " + input_time + " " + str(package.status))
                                print("-----------------------------------------------------------------------------------")
                                print("")
                               
                                exit()
                            except ValueError:
                                print("")
                                print("Entry invalid.")
                                print("")
                    else:
                        exit()
        elif(answer == "exit"):
            exit()
            
