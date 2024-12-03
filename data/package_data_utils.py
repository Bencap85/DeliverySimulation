import csv
from entities.Package import Package
from entities.Status import Status


def loadPackageData(file_name, hash_table):
    with open(file_name) as file:
        packageData = csv.reader(file, delimiter=',')
        for row in packageData:
            package_id = row[0]
            address = row[1]
            city = row[2]
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]
            status = Status.AT_HUB

            package = Package(package_id, address, deadline, city, zip_code, weight, status)
            hash_table.put(package_id, package)

