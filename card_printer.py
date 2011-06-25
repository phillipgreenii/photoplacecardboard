from reportlab.lib import pagesizes
import math

class CardPrinter:
    def __init__(self, page_sizes, card_sizes, minimum_card_spacing = 0.06125 * pagesizes.inch, page_margins = 4 * (0.5 * pagesizes.inch, )):
        (self.page_width, self.page_height) = page_sizes
        (self.card_width, self.card_height) = card_sizes
        (page_margin_top, page_margin_left, page_margin_bottom, page_margin_right) = page_margins
        (self.cards_per_row, self.cards_per_column) = \
                             (math.floor((self.page_width - page_margin_left - page_margin_right) / (self.card_width + minimum_card_spacing)),\
                              math.floor((self.page_height- page_margin_top - page_margin_bottom) / (self.card_height + minimum_card_spacing)))
        self.x_margin = page_margin_left
        self.x_offset = self.card_width + minimum_card_spacing
        self.y_margin = page_margin_top
        self.y_offset = self.card_height + minimum_card_spacing
        
    def print_on_front_page(self,canvas, card, row_index, column_index):
        (card_x, card_y) = \
                 (self.x_margin + (self.x_offset * column_index),\
                  (self.page_height - self.card_height) - (self.y_margin + (self.y_offset * row_index)))
        # print background image
        canvas.drawInlineImage(card.image, card_x, card_y, width = self.card_width, height = self.card_height)
        # crop edge
        canvas.saveState()
        canvas.setStrokeColorRGB(1,1,1)
        canvas.setLineWidth(0.125 * pagesizes.inch)
        canvas.rect(card_x, card_y, self.card_width, self.card_height)
        canvas.restoreState()
        # add name, if it exists
        if card.name is not None:
            canvas.drawCentredString(card_x + self.card_width/2.0,card_y + self.card_height/2.0, card.name)
        # add border
        canvas.saveState()
        canvas.setStrokeColorRGB(0,0,0)
        canvas.rect(card_x, card_y, self.card_width, self.card_height)
        canvas.restoreState()
        
    def print_on_back_page(self, canvas, card, row_index, column_index):
        (card_x, card_y) = \
                 ((self.page_width - self.card_width) - (self.x_margin + (self.x_offset * column_index)),\
                  (self.page_height - self.card_height) - (self.y_margin + (self.y_offset * row_index)))
        # add table name, if it exists
        if card.table_name is not None:
            canvas.drawCentredString(card_x + (self.card_width/2.0), card_y + (self.card_height / 2.0),str(card.table_name))
        # add position
        canvas.saveState()
        canvas.setFontSize(7)
        canvas.drawString(card_x + 10, card_y + 10,str(card.position))#TODO don't hardcode offset
        canvas.restoreState()
        # add border
        canvas.setStrokeColorRGB(0,0,0)
        canvas.rect(card_x, card_y, self.card_width, self.card_height)
