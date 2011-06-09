#!/usr/bin/env python


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
unusedArea = ( (845, 1600) , (1245, 2400) )

cardHeightPixels = pictureHeight / verticalCardsCount
cardWidthPixels = pictureWidth / horizontalCardsCount

cards = []
for i in range(verticalCardsCount):
    for j in range(horizontalCardsCount):
        cards.append( ((i * cardHeightPixels, j * cardWidthPixels),\
 ((i+1) * cardHeightPixels, (j+1) * cardWidthPixels) ) )
print len(cards)
