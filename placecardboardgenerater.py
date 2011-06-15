#!/usr/bin/env python

from area import Area
import Image, ImageDraw, ImageFont
import csv

#################
## FUNCTIONS

def parse_people(file_name,
                 accepted_column_name ="RSVP",
                 accepted_value="Accepted",
                 placecard_name_column_name="PlaceCard",
                 table_name_column_name="Table_Name"):
    invitationListReader = csv.reader(open('invitationlist.csv', 'rb'))
    column_names = invitationListReader.next()

    accepted_column_index = column_names.index(accepted_column_name)
    placecard_name_column_index= column_names.index(placecard_name_column_name)
    table_name_column_index = column_names.index(table_name_column_name)
    
    people = []
    for row in invitationListReader:
        if row[accepted_column_index] == accepted_value:
            people.append((row[placecard_name_column_index], row[table_name_column_index]))
    people.sort()
    return people

def generate_cards(verticalCardsCount, horizontalCardsCount, cardHeightPixels, cardWidthPixels):
    cards = []
    for i in range(verticalCardsCount):
        for j in range(horizontalCardsCount):
            point = (j * cardWidthPixels, i * cardHeightPixels)
            cards.append(Area(point, cardHeightPixels, cardWidthPixels))
    return cards

def filter_usable_cards(cards, *unusableAreas):
    if len(unusableAreas) <= 0:
        return cards
    else:
        filtered_cards =  filter(lambda a: not a.intersects(unusableAreas[0]), cards)
        return filter_usable_cards(filtered_cards, *unusableAreas[1:])


#################
## PARAMETERS

verticalCardsCount = 15
horizontalCardsCount = 15

cardHeight = 2
cardWidth = 3
spaceBetweenCards = 0.125

invitation_list_name = 'invitationlist.csv'
picture_name = 'picture.jpg'

areaOfBrideAndGroom = Area( (765, 1610) , 740, 330)
print "areaOfBrideAndGroom: %s " % areaOfBrideAndGroom

#################
## INTERMEDIATE VALUES

oim = Image.open(picture_name)
im = oim.convert("L") 

pictureWidth, pictureHeight = im.size

cardHeightPixels = pictureHeight / verticalCardsCount
cardWidthPixels = pictureWidth / horizontalCardsCount
print "cardHeightPixels: %i" % cardHeightPixels
print "cardWidthPixels: %i" % cardWidthPixels


#################
## WORK

people = parse_people(invitation_list_name, placecard_name_column_name='Party_Name')
print "people count: %i" % len(people)

cards = generate_cards(verticalCardsCount, horizontalCardsCount, cardHeightPixels, cardWidthPixels)
print "cards count: %i" % len(cards)

usable_cards = filter_usable_cards(cards, areaOfBrideAndGroom)
print "usable cards count: %i" % len(usable_cards)


im.crop(areaOfBrideAndGroom.box).save("tmp/brideAndGroomArea.jpg", "JPEG")

font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)
for (i,card) in enumerate(usable_cards):
    part = im.crop(card.box)
    total = 0
    count = 0
    for p in part.getdata():
        total+= p
        count+= 1
    avg = total/count
    if avg > 127:
        color = 0
    else:
        color = 255 
    personname = "John Doe"
    draw = ImageDraw.Draw(part)
    (w,h) = draw.textsize(personname, font=font)
    pw = cardWidthPixels/2 - w/2
    ph = cardHeightPixels/2 - h/2
    draw.text((pw,ph), personname, font=font, fill=color)
    del draw
    part.save("tmp/part%04i.jpg" % i, "JPEG")
