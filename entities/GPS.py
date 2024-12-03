from entities.Package import Package


class GPS:
    def __init__(self, distance_data, address_list):
        self.distance_data = distance_data
        self.address_list = address_list

    def distance_between(self, address_one, address_two):
        i = self.address_list.index(address_one)
        j = self.address_list.index(address_two)

        if self.distance_data[i][j] is not None:
            return self.distance_data[i][j]
        elif self.distance_data[j][i] is not None:
            return self.distance_data[j][i]
        else:
            return -1.0

    def get_actual_address(self, address):
        actual_address = address
        index = next((i for i, s in enumerate(self.address_list) if address in s), -1)
        actual_address = self.address_list[index]
        if actual_address is None:
            print("NO ACTUAL ADDRESS FOUND FOR ", address)
        return actual_address

    def nearest_neighbor(self, stops):
        route = []
        start_address = stops[0]
        route.append(start_address)

        while len(route) < len(set(stops)):
            current_stop = route[-1]
            min_distance = float('inf')
            nearest_neighbor = None

            for i in range(len(stops)):
                if stops[i] in route:
                    continue
                if current_stop == stops[i]:
                    continue

                if self.distance_between(current_stop, stops[i]) < min_distance:
                    nearest_neighbor = stops[i]
                    min_distance = self.distance_between(current_stop, stops[i])

            route.append(nearest_neighbor)

        return route

    def generate_route(self, address_list):
        route = self.nearest_neighbor(address_list)
        # route = address_list
        return route
