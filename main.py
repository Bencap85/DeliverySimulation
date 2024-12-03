import datetime

from data.address_data_utils import loadAddressData
from data.distance_data_utils import loadDistanceData
from data.package_data_utils import loadPackageData
from entities.GPS import GPS
from entities.HashTable import HashTable
from entities.Status import Status
from entities.Package import Package
from entities.Truck import Truck
from entities.Driver import Driver


# https://svn.blender.org - Special characters to represent colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'  # S


# Selects color of printed text based on status of package
def get_color(status):
    color = bcolors.FAIL
    if status == Status.EN_ROUTE:
        color = bcolors.WARNING
    if status == Status.DELIVERED:
        color = bcolors.OKGREEN

    return color


# Returns a list of packages to be loaded onto truck 1
def truck_one_packages():
    packages = []
    packages.append(hash_table.get('29'))
    packages.append(hash_table.get('7'))

    # Must be delivered together
    packages.append(hash_table.get('13'))
    packages.append(hash_table.get('15'))
    packages.append(hash_table.get('19'))
    packages.append(hash_table.get('14'))
    packages.append(hash_table.get('20'))
    packages.append(hash_table.get('16'))

    packages.append(hash_table.get('31'))

    packages.append(hash_table.get('40'))

    packages.append(hash_table.get('37'))
    packages.append(hash_table.get('22'))

    packages.append(hash_table.get('34'))

    packages.append(hash_table.get('2'))
    packages.append(hash_table.get('33'))

    packages.append(hash_table.get('30'))


    return packages


# Returns a list of packages to be loaded onto truck 2
def truck_two_packages():
    packages = []

    # Must be on truck 2
    packages.append(hash_table.get('18'))
    packages.append(hash_table.get('36'))
    packages.append(hash_table.get('38'))
    packages.append(hash_table.get('3'))

    packages.append(hash_table.get('1'))

    packages.append(hash_table.get('39'))

    packages.append(hash_table.get('8'))

    packages.append(hash_table.get('17'))
    packages.append(hash_table.get('12'))
    packages.append(hash_table.get('21'))
    packages.append(hash_table.get('5'))
    packages.append(hash_table.get('10'))
    packages.append(hash_table.get('6'))
    packages.append(hash_table.get('25'))

    return packages

# Returns a list of packages to be loaded onto truck 3
def truck_three_packages():
    packages = []
    packages.append(hash_table.get('28'))
    packages.append(hash_table.get('9'))
    packages.append(hash_table.get('32'))
    packages.append(hash_table.get('4'))
    packages.append(hash_table.get('24'))

    packages.append(hash_table.get('23'))
    packages.append(hash_table.get('26'))

    packages.append(hash_table.get('27'))
    packages.append(hash_table.get('35'))
    packages.append(hash_table.get('11'))

    return packages


# Initializes packages with their statuses before they are loaded on the trucks
def initialize_packages_in_hub():
    for i in range(1, 41):
        package = hash_table.get(str(i))

        # Accounts for packages delayed in flight, not arriving until 9:05
        if i in [6, 25, 28, 32]:
            package.status = Status.DELAYED_IN_FLIGHT
            package.save(datetime.time(9, 4, 0))
            package.status = Status.AT_HUB
            package.save(datetime.time(9, 5, 0))

        else:
            package.save(datetime.time(7, 59, 59))

# Presents menu options to viewer, returns user's menu item selection
def present_menu():
    selection = input("""
    
    Menu:
          
        1: To view an individual package's status at any given time
            
        2: To view all packages' statuses at any given time
        
        3: To view the total mileage traveled by all trucks
        
        4: Exit
    
""")
    return selection


# Prints statuses of all packages at a particular point in time
def print_status_of_all_packages_at(time):
    for i in range(1, 41):
        package = hash_table.get(str(i))

        instance = package.get_instance_at_time(time)
        color = get_color(instance.status)
        if instance.status == Status.DELIVERED:
            print(color, "Package", instance.package_id, "DELIVERED to", instance.address, "by Truck",
                  package.truck_number, "at", instance.last_status_change_time, ", Deadline: ", instance.deadline,
                  bcolors.ENDC)
        elif instance.status == Status.EN_ROUTE:
            print(color, "Package", instance.package_id, "EN_ROUTE to", instance.address, "on Truck",
                  package.truck_number, "since",
                  instance.last_status_change_time, ", Deadline: ", instance.deadline,
                  bcolors.ENDC)
        elif instance.status == Status.DELAYED_IN_FLIGHT:
            print(color, "Package", instance.package_id, str(instance.status)[7:], "until 09:05:00",
                  ", Destination:", instance.address, ", Deadline: ", instance.deadline, bcolors.ENDC)
        else:
            print(color, "Package", instance.package_id, str(instance.status)[7:], "since", instance.last_status_change_time,
                  ", Destination:", instance.address, ", Deadline: ", instance.deadline, bcolors.ENDC)


# Sets up simulation, initializes trucks/packages

# Data structures that hold data read from CSV files
hash_table = HashTable(40)
address_list = []
distance_list = []

# Loads data from CSV files into respective data structures
loadPackageData('data/package_data.csv', hash_table)
loadAddressData('data/address_data.csv', address_list)
loadDistanceData('data/distance_data.csv', distance_list)

# Gives packages an initial status of 'AT HUB'
initialize_packages_in_hub()

# Sets Package #9 to correct to 410 State St at 10:20
hash_table.get('9').address = "410 S State St"
hash_table.get('9').save(datetime.time(10, 20, 0))
hash_table.get('9').address = '300 State St'

# Initialize a GPS object. This object contains the logic related to route planning. It takes a distance matrix and
# an address list as arguments to define its route-planning domain. The main interface is through the generate_route
# method, in which the GPS takes a list of addresses and sorts them into an optimized route
gps = GPS(distance_list, address_list)

driver_one = Driver()
driver_two = Driver()

truck_one = Truck(1, datetime.time(8, 0, 0), driver_one, gps)
truck_two = Truck(2, datetime.time(9, 5, 0),  driver_two, gps)

# Truck 1 is loaded with preassigned packages returned by truck_one_packages() and leaves at 8:00
truck_one.load_packages(truck_one_packages(), datetime.time(8, 0, 0))

# Truck 2 is loaded with preassigned packages returned by truck_two_packages() and leaves the hub at 9:05 due to
# certain onboard packages being delayed until that time
truck_two.load_packages(truck_two_packages(), datetime.time(9, 5, 0))

# Generates optimal route
truck_one.generate_route()
truck_two.generate_route()

# Executes route
truck_one.deliver()
truck_two.deliver()

# Set up/send out truck 3
truck_three = Truck(3, truck_one.current_time.time(), driver_one, gps)
# Waits to send out Truck 3 until corrected address for Package #9 comes in at 10:20
if truck_three.current_time < datetime.time(10, 20, 0):
    truck_three.START_TIME = datetime.time(10, 20, 0)
else:
    truck_three.START_TIME = truck_one.current_time.time()

# truck_three.START_TIME = truck_one.current_time.time()
truck_three.current_time = truck_three.START_TIME

# Correct Package #9 address
hash_table.get('9').address = '410 State St'

# Loads preassigned packages into Truck 3
truck_three.load_packages(truck_three_packages(), truck_three.current_time)

# Generates optimal route
truck_three.generate_route()

# Executes route
truck_three.deliver()

# Start CLI to view details of the run
print("Route Optimization Simulation")
print()
print(bcolors.OKCYAN, "All packages delivered successfully. Total mileage: ",
      (truck_one.total_miles + truck_two.total_miles + truck_three.total_miles), bcolors.ENDC)
print()

selection = 0

while selection != '4':
    # Shows menu and returns user input
    selection = present_menu()

    # If "To view an individual package's status at any given time"
    if selection == '1':
        valid = False
        package_id = ''
        # Get package ID
        while not valid:
            package_id = input("Enter the package id: ")
            if package_id is None or package_id == '' or int(package_id) not in [i for i in range(1, 41)]:
                print("Invalid package id. Try again\n")
                continue
            else:
                valid = True

        package = hash_table.get(package_id)
        valid = False
        # Get time
        while not valid:
            input_time = input("Enter the time (HH:MM): ")
            if (len(input_time.split(':')) != 2
                or not 0 < int(input_time.split(':')[0]) < 25) \
                    or not 0 <= int(input_time.split(':')[1]) < 60:
                print("Invalid time. Try again\n")
                continue

            hours = input_time.split(':')[0]
            minutes = input_time.split(':')[1]
            seconds = 0

            time = datetime.time(int(hours), int(minutes), int(seconds))

            instance = package.get_instance_at_time(time)
            color = get_color(instance.status)

            if instance.status == Status.DELIVERED:
                print(color, "Package", instance.package_id, "DELIVERED to", instance.address, "by Truck", package.truck_number, "at", instance.last_status_change_time, ", Deadline: ", instance.deadline, bcolors.ENDC)
            elif instance.status == Status.EN_ROUTE:
                print(color, "Package", instance.package_id, "EN_ROUTE to", instance.address, "on Truck", package.truck_number, "since",
                      instance.last_status_change_time, ", Deadline: ", instance.deadline,
                      bcolors.ENDC)
            elif instance.status == Status.DELAYED_IN_FLIGHT:
                print(color, "Package", instance.package_id, str(instance.status)[7:], "until 09:05:00",
                      ", Destination:", instance.address, ", Deadline: ", instance.deadline, bcolors.ENDC)
            else:
                print(color, "Package", instance.package_id, "AT_HUB since", instance.last_status_change_time, ", Destination:", instance.address, ", Deadline: ", instance.deadline, bcolors.ENDC)

            valid = True

    # If "To view all packages' statuses at any given time"
    elif selection == '2':
        valid = False
        # Get time
        while not valid:
            input_time = input("Enter the time (HH:MM): ")
            if (len(input_time.split(':')) != 2
                or not 0 < int(input_time.split(':')[0]) < 25) \
                    or not 0 <= int(input_time.split(':')[1]) < 60:
                print("Invalid time. Try again\n")
                continue

            hours = input_time.split(':')[0]
            minutes = input_time.split(':')[1]
            seconds = 0

            time = datetime.time(int(hours), int(minutes), int(seconds))

            valid = True

            print_status_of_all_packages_at(time)

    # If "To view the total mileage traveled by all trucks"
    elif selection == '3':
        print(bcolors.OKCYAN)
        print("Truck 1 travelled", "{:.2f}".format(truck_one.total_miles), "miles")
        print("Truck 2 travelled", "{:.2f}".format(truck_two.total_miles), "miles")
        print("Truck 3 travelled", "{:.2f}".format(truck_three.total_miles), "miles")
        print("-----------------------------------------------")
        print("Total mileage traveled by all trucks: ",
              "{:.2f}".format(truck_one.total_miles + truck_two.total_miles + truck_three.total_miles), "miles")
        print(bcolors.ENDC)

    # If "exit"
    elif selection == '4':
        print(bcolors.OKCYAN, "Goodbye!", bcolors.ENDC)
        exit(0)

    # If input was not 1, 2, 3, or 4, ask to try again
    else:
        print("Please enter 1, 2, 3, or 4")
        continue
