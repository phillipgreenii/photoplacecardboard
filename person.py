class Person:
    def __init__(self, first_name, last_name, placecard_name, table_name):
        self.first_name = first_name
        self.last_name = last_name
        self.placecard_name = placecard_name
        self.table_name = table_name
        
    def __repr__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __lt__(self,other):
        if self.last_name < other.last_name:
            return True
        if self.last_name == other.last_name:
            return self.first_name < other.first_name
        return False

