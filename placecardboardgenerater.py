#!/usr/bin/env python

from area import Area
from card import Card
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

def generate_printing_areas(verticalAreaCount, horizontalAreaCount, areaHeightPixels, areaWidthPixels):
    areas = []
    counter = 0
    for i in range(verticalAreaCount):
        for j in range(horizontalAreaCount):
            point = (j * areaWidthPixels, i * areaHeightPixels)
            areas.append((counter, Area(point, areaHeightPixels, areaWidthPixels)))
            counter += 1
    return areas

def filter_usable_areas(areas, *unusableAreas):
    if len(unusableAreas) <= 0:
        return areas
    else:
        filtered_areas =  filter(lambda a: not a[1].intersects(unusableAreas[0]), areas)
        return filter_usable_areas(filtered_areas, *unusableAreas[1:])

def generate_cards(areas, people, font):
    extended_people = people + ( (len(areas) - len(people)) * [None])
    cards = []
    for (parea,person) in zip(areas, extended_people):
        position,area = parea
        part = im.crop(area.box)
        name = None
        table_name = None
        if person is not None:
            name,table_name = person 
            add_name_to_image(part, name, font)
        part.save("tmp/part%04i.jpg" % position, "JPEG")
        cards.append(Card(position,part,name, table_name))
    return cards


def add_name_to_image(image, name, font):
       draw = ImageDraw.Draw(image)
       (w,h) = draw.textsize(name, font=font)
       pw = cardWidthPixels/2 - w/2
       ph = cardHeightPixels/2 - h/2
       draw.text((pw,ph), name, font=font, fill=determine_font_color(image))
       del draw
                
def determine_font_color(image):
    pixel_data = list(image.getdata())
    avg = sum(pixel_data) / len(pixel_data)
    if avg > 127:
        return   0 #BLACK
    else:
        return 255 #WHITE 
    


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

font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)

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

areas = generate_printing_areas(verticalCardsCount, horizontalCardsCount, cardHeightPixels, cardWidthPixels)
print "areas count: %i" % len(areas)

usable_areas = filter_usable_areas(areas, areaOfBrideAndGroom)
print "usable areas count: %i" % len(usable_areas)


im.crop(areaOfBrideAndGroom.box).save("tmp/brideAndGroomArea.jpg", "JPEG")

cards = generate_cards(usable_areas, people, font)
print "cards count: %i" % len(cards)

