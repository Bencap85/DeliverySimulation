import csv

def loadAddressData(file_name, list):
    with open(file_name) as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            list.append(row.pop(0))