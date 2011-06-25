#!/usr/bin/env python

from area import Area
from card import Card
from person import Person
from card_printer import CardPrinter
import Image
import csv

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import pagesizes


#################
## FUNCTIONS

def parse_people(file_name,
                 first_name_column_name = "First_Name",
                 last_name_column_name = "Last_Name",
                 accepted_column_name ="RSVP",
                 accepted_value="Accepted",
                 placecard_name_column_name="PlaceCard",
                 table_name_column_name="Table_Name"):
    invitationListReader = csv.reader(open('invitationlist.csv', 'rb'))
    column_names = invitationListReader.next()

    first_name_column_index = column_names.index(first_name_column_name)
    last_name_column_index = column_names.index(last_name_column_name)
    accepted_column_index = column_names.index(accepted_column_name)
    placecard_name_column_index= column_names.index(placecard_name_column_name)
    table_name_column_index = column_names.index(table_name_column_name)
    
    people = []
    for row in invitationListReader:
        if row[accepted_column_index] == accepted_value:
            people.append(Person(row[first_name_column_index], row[last_name_column_index], row[placecard_name_column_index], row[table_name_column_index]))
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

def generate_cards(areas, people):
    extended_people = people + ( (len(areas) - len(people)) * [None])
    cards = []
    for (parea,person) in zip(areas, extended_people):
        position,area = parea
        part = im.crop(area.box)
        name = None
        table_name = None
        if person is not None:
            name =  person.placecard_name
            table_name = person.table_name
        imageName = "tmp/part%04i.jpg" % position
        part.save(imageName, "JPEG") 
        cards.append(Card(position,part.size,imageName,name, table_name))
    return cards

def generate_pages(card_sizes,cards, filename="placecards.pdf"):
    pagesize = pagesizes.portrait( ( 8.5 * pagesizes.inch, 11 * pagesizes.inch))
    pdf = Canvas(filename, pagesize=pagesize)
    pdf.setAuthor('placecardboardgenerate.py')
    pdf.setSubject('wedding placecards')
    pdf.setTitle('Placecards for Wedding Reception')
    pdf.setKeywords(('wedding', 'placecards'))

    adjusted_card_sizes = (card_sizes[0] * pagesizes.inch, card_sizes[1] * pagesizes.inch)
    card_printer = CardPrinter(pagesize,adjusted_card_sizes)

    (cardsPerRow,rowsPerPage) = (card_printer.cards_per_row, card_printer.cards_per_column)

    (page_width, page_height) = pagesize

    groupedCards = group_cards(cards, cardsPerRow, rowsPerPage)
    for (page_index,pageOfCards) in enumerate(groupedCards):
        for (row_index,rowOfCards) in enumerate(pageOfCards):
            for (column_index,card) in enumerate(rowOfCards):
                card_printer.print_on_front_page(pdf,card,row_index, column_index)
        pdf.drawCentredString(page_width/2.0,20,"front of page %i" % (page_index + 1))
        pdf.showPage()
        for (row_index,rowOfCards) in enumerate(pageOfCards):
            for (column_index,card) in enumerate(rowOfCards):
                card_printer.print_on_back_page(pdf,card,row_index, column_index)                
        pdf.drawCentredString(page_width/2.0,20,"back of page %i" % (page_index + 1))
        pdf.showPage()

    pdf.save()


def group_cards(cards, cardsPerRow, rowsPerPage):
    pages = []
    page = []
    row = []
    for card in cards:
        row.append(card)
        if len(row) == cardsPerRow:
            page.append(row)
            row = []
            if len(page) == rowsPerPage:
                pages.append(page)
                page = []
    # add left overs
    if len(row) > 0:
        page.append(row)
    if len(page) > 0:
        pages.append(page)
    return pages

def generate_key(verticalCardsCount,horizontalCardsCount,cards, filename="key.pdf", page_margins = 4 * (0.5 * pagesizes.inch, )):
    (page_margin_top, page_margin_left, page_margin_bottom, page_margin_right) = page_margins
    padding = 0.0625 * pagesizes.inch

    spaces = (verticalCardsCount * horizontalCardsCount) * [None,]
    for card in cards:
        spaces[card.position] = card

    pagesize = pagesizes.landscape( ( 8.5 * pagesizes.inch, 11 * pagesizes.inch))
    pdf = Canvas(filename, pagesize=pagesize)
    pdf.setAuthor('placecardboardgenerate.py')
    pdf.setSubject('wedding placecards key')
    pdf.setTitle('Key for Placecards for Wedding Reception')
    pdf.setKeywords(('wedding', 'placecards'))

    (page_width, page_height) = pagesize

    pdf.drawCentredString(page_width/2.0,20,"key of place cards")

    thumbnail_width = ((page_width - page_margin_left - page_margin_right) - (padding * (horizontalCardsCount - 1))) / horizontalCardsCount
    thumbnail_height = ((page_height - page_margin_top - page_margin_bottom) - (padding * (verticalCardsCount - 1))) / verticalCardsCount


    x_margin = page_margin_left
    x_offset = thumbnail_width + padding
    y_margin = page_margin_top
    y_offset = thumbnail_height + padding


    for row_index in range(verticalCardsCount):
        for column_index in range(horizontalCardsCount):
            position = (row_index * horizontalCardsCount) +  column_index
            card = spaces[position]
            (card_x, card_y) = \
                 (x_margin + (x_offset * column_index),\
                  (page_height - thumbnail_height) - (y_margin + (y_offset * row_index)))
            
            if card is not None:
                pdf.drawInlineImage(card.image, card_x, card_y, width = thumbnail_width, height = thumbnail_height)
                pdf.drawCentredString(card_x + thumbnail_width/2.0,card_y + thumbnail_height/2.0, str(card.position))
    
    pdf.showPage()
    pdf.save()



#################
## PARAMETERS

posterWidth, posterHeight = (36,24) #inches
print "posterHeight: %i" % posterHeight
print "posterWidth %i" % posterWidth

verticalCardsCount = 15
horizontalCardsCount = 15

spaceBetweenCards = 0.125

invitation_list_name = 'invitationlist.csv'
picture_name = 'picture.jpg'

areaOfBrideAndGroom = Area( (765, 1610) , 740, 330)
print "areaOfBrideAndGroom: %s " % areaOfBrideAndGroom

#################
## INTERMEDIATE VALUES

oim = Image.open(picture_name)
im = oim.convert("L") 

pictureWidthPixels, pictureHeightPixels = im.size
print "pictureHeightPixels: %i" % pictureHeightPixels
print "pictureWidthPixels: %i" % pictureWidthPixels

ppi = ((pictureWidthPixels / posterWidth) * (pictureHeightPixels / posterHeight))**(0.5)

print "PPI: %0.3f" % ppi


cardHeight = 1.0 * posterHeight / verticalCardsCount
cardWidth = 1.0 * posterWidth / horizontalCardsCount
print "cardHeight: %0.3f" % cardHeight
print "cardWidth: %0.3f" % cardWidth

cardHeightPixels = pictureHeightPixels / verticalCardsCount
cardWidthPixels = pictureWidthPixels / horizontalCardsCount
print "cardHeightPixels: %i" % cardHeightPixels
print "cardWidthPixels: %i" % cardWidthPixels


#################
## WORK

people = parse_people(invitation_list_name, placecard_name_column_name='Party_Name', table_name_column_name='Group')#FIXME use correct column names
print "people count: %i" % len(people)

areas = generate_printing_areas(verticalCardsCount, horizontalCardsCount, cardHeightPixels, cardWidthPixels)
print "areas count: %i" % len(areas)

usable_areas = filter_usable_areas(areas, areaOfBrideAndGroom)
print "usable areas count: %i" % len(usable_areas)


im.crop(areaOfBrideAndGroom.box).save("tmp/brideAndGroomArea.jpg", "JPEG")

cards = generate_cards(usable_areas, people)
print "cards count: %i" % len(cards)

generate_pages((cardWidth, cardHeight), cards)
generate_key(verticalCardsCount,horizontalCardsCount,cards)
