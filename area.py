class Area:
    def __init__(self, upperLeftPoint, height, width):
        self.upperLeftPoint = upperLeftPoint
        self.upperRightPoint = (upperLeftPoint[0]+ width, upperLeftPoint[1] )
        self.lowerLeftPoint = (upperLeftPoint[0], upperLeftPoint[1]+ height)
        self.lowerRightPoint = (upperLeftPoint[0] + width, upperLeftPoint[1] + height)
        self.corners = ( self.upperLeftPoint, self.upperRightPoint, self.lowerLeftPoint, self.lowerRightPoint)
        self.height = height
        self.width = width
    
    def intersectsPoint(self, point):
        return ( self.upperLeftPoint[0] <=  point[0] and point[0] <= self.upperLeftPoint[0] + self.width ) \
            and (self.upperLeftPoint[1] <=  point[1] and point[1] <= self.upperLeftPoint[1] + self.height )

    def intersects(self, area):
        for corner in self.corners:
            if area.intersectsPoint(corner):
                return True
        return False
    
    def __repr__(self):
        return str(self.corners)
