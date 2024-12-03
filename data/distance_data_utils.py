import csv


def loadDistanceData(file_name, list):
    with open(file_name) as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            list.append([])
            for entry in row:
                if(entry == ''):
                    list[-1].append(None)
                else:
                    list[-1].append(float(entry))


