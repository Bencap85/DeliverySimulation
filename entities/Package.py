from datetime import datetime
import entities.Status
from entities.Status import Status


class Package:
    def __init__(self, package_id, address=None, deadline=None, city=None, zip_code=None, weight=None, status=Status.AT_HUB):
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.status = status
        self.history = {}
        self.last_status_change_time = None
        self.truck_number = -1

    def __str__(self):
        return f'{self.package_id}: {self.address}'

    def save(self, time):
        copy = Package(self.package_id, self.address, self.deadline, self.city, self.zip_code, self.weight, self.status)
        copy.last_status_change_time = time
        self.history[time] = copy

    def get_instance_at_time(self, time):

        keys = list(self.history.keys())
        keys.sort()

        if time < keys[0]:
            return self.history[keys[0]]

        if time > keys[len(keys) - 1]:
            return self.history[keys[len(keys) - 1]]

        for i in range(len(keys)):

            if keys[i].hour == time.hour and keys[i].minute == time.minute and keys[i].second == time.second:
                return self.history[keys[i]]

            if keys[i] < time < keys[i + 1]:
                return self.history[keys[i]]


        return None