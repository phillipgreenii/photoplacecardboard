#!/usr/bin/env python

from area import Area
import Image

verticalCardsCount = 15
horizontalCardsCount = 15

totalCardsCount = verticalCardsCount * horizontalCardsCount

print totalCardsCount

cardHeight = 2
cardWidth = 3
spaceBetweenCards = 0.125

im = Image.open("picture.jpg")

pictureHeight = im.size[1]
pictureWidth = im.size[0]

#(0,0) is upper left corner of picture
unusedArea = Area( (765, 1610) , 740, 330)

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

ignoredCards =  filter(lambda a: a.intersects(unusedArea), cards)

unusedAreaPicture = im.crop((unusedArea.upperLeftPoint[0],unusedArea.upperRightPoint[1], unusedArea.lowerRightPoint[0], unusedArea.lowerRightPoint[1]))
unusedAreaPicture.save("tmp/nocardarea.jpg", "JPEG")

for (i,card) in enumerate(printableCards):
    box = (card.upperLeftPoint[0],card.upperRightPoint[1], card.lowerRightPoint[0], card.lowerRightPoint[1])
    part = im.crop(box)
    part.save("tmp/part%04i.jpg" % i, "JPEG")
