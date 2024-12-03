

class HashTable:

    load_factor_threshold = 0.8

    def __init__(self, size=10):
        self.num_items = 0
        self.size = size
        self.array = []
        for i in range(self.size):
            self.array.append([])

    def get(self, key):
        location = self._get_hash(key)
        sub_array = self.array[location]

        for i in range(len(sub_array)):
            if sub_array[i].package_id == key:
                return sub_array[i]

        return None

    def put(self, key, value):
        location = self._get_hash(key)
        sub_array = self.array[location]

        field_name = "package_id"

        for entry in sub_array:
            if entry.package_id is not None and entry.package_id == key: # Value already exists
                entry = value
                return

        self.array[location].append(value)
        self.num_items += 1

        load_factor = self.num_items / self.size
        if load_factor > self.load_factor_threshold:
            self._grow()


    def _grow(self):
        increase = len(self.array)
        self.size += increase
        for i in range(increase):
            self.array.append([])

        field_name = "package_id"

        for sub_array in self.array:
            for entry in sub_array:
                self.put(entry.package_id, entry)


    def _get_hash(self, key):
        location = hash(key) % self.size
        return location

    def __str__(self):
        s = ""
        for i in range(len(self.array)):
            s += "Bucket " + str(i) + ": "
            for j in range(len(self.array[i])):
                p = self.array[i][j]
                s += str(p) + ", "
            s += "\n"
        return s



