import datetime

from entities.Status import Status


class Truck:
    MILES_PER_HOUR = 18
    MAX_PACKAGES = 16
    START_TIME = None
    HUB_ADDRESS = None

    def __init__(self, number, start_time, driver=None, gps=None):

        self.number = number
        self.route = []
        self.driver = driver
        self.packages = []
        self.total_time = 0
        self.total_miles = 0
        self.START_TIME = start_time
        self.current_time = self.START_TIME
        self.current_address = gps.get_actual_address('\"Western Governors University 4001 South 700 East')
        self.HUB_ADDRESS = self.current_address
        self.gps = gps

    def load_packages(self, packages, time):

        if (len(self.packages) + len(packages)) > self.MAX_PACKAGES:
            raise Exception('Too many packages')

        self.packages.extend(packages)

        for package in self.packages:
            package.truck_number = self.number
            package.status = Status.EN_ROUTE
            package.save(time)


    def generate_route(self):
        stops = [self.current_address]
        for package in self.packages:
            if package.address not in stops:
                stops.append(self.gps.get_actual_address(package.address))

        self.route = self.gps.generate_route(stops)
        self.route.append(self.gps.get_actual_address('\"Western Governors University 4001 South 700 East'))


    def deliver(self):

        for i in range(1, len(self.route)):
            next_address = self.route[i]

            this_address_packages = []
            for package in self.packages:
                actual_address = self.gps.get_actual_address(package.address)

                if actual_address in next_address:
                    this_address_packages.append(package)

            elapsed_hours = float(self.gps.distance_between(self.current_address, next_address)) / float(
                self.MILES_PER_HOUR)

            dummy = datetime.datetime(1, 1, 1, self.current_time.hour, self.current_time.minute,
                                      self.current_time.second) + datetime.timedelta(hours=elapsed_hours)
            self.current_time = dummy

            self.total_miles += self.gps.distance_between(self.current_address, next_address)

            for package in this_address_packages:
                package.status = Status.DELIVERED
                package.save(self.current_time.time())
                # print("Delivered ", package.package_id, " to ", package.address, " at ", self.current_time.time())


            self.current_address = next_address

