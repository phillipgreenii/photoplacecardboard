#!/usr/bin/env python

from area import Area


verticalCardsCount = 15
horizontalCardsCount = 15

totalCardsCount = verticalCardsCount * horizontalCardsCount

print totalCardsCount

cardHeight = 2
cardWidth = 3
spaceBetweenCards = 0.125

pictureHeight = 2400
pictureWidth = 3600

#(0,0) is upper left corner of picture
unusedArea = Area( (845, 1600) , 800, 400)
print "unusedArea: %s " % unusedArea


cardHeightPixels = pictureHeight / verticalCardsCount
cardWidthPixels = pictureWidth / horizontalCardsCount

print "cardHeightPixels: %f" % cardHeightPixels
print "cardWidthPixels: %f" % cardWidthPixels

cards = []
for i in range(verticalCardsCount):
    for j in range(horizontalCardsCount):
        point = (j * cardWidthPixels, i * cardHeightPixels)
        cards.append(Area(point, cardHeightPixels, cardWidthPixels))
print len(cards)

printableCards = filter(lambda a: not a.intersects(unusedArea), cards)
print len(printableCards)


