class Card:
    def __init__(self, position, size, image, name = None, table_name = None):
        self.position = position
        self.image = image
        self.size = size
        self.name = name
        self.table_name = table_name
        
    def __repr__(self):
        if self.name is None:
            return "card (%i) for no one" % self.position
        else :
            return "card (%i) for %s at %s" % (self.position, self.name, self.table_name or "*unknown table*")
