import random


class Card:
    def __init__(self, card_id):
        self.card_id = card_id
        self.faceup = True

    def get_val(self):
        return int(self.card_id[-2:])

    def get_suit(self):
        return self.card_id[0]

    def get_path(self):
        return 'myresources/cards/' + self.card_id + '.bmp'


class Deck:
    __all_cards = ['c01', 'c02', 'c03', 'c04', 'c05', 'c06', 'c07', 'c08', 'c09', 'c10', 'c11', 'c12', 'c13', 'h01',
                   'h02', 'h03', 'h04', 'h05', 'h06', 'h07', 'h08', 'h09', 'h10', 'h11', 'h12', 'h13', 's01', 's02',
                   's03', 's04', 's05', 's06', 's07', 's08', 's09', 's10', 's11', 's12', 's13', 'd01', 'd02', 'd03',
                   'd04', 'd05', 'd06', 'd07', 'd08', 'd09', 'd10', 'd11', 'd12', 'd13']

    def __init__(self):
        self.cards = self.__all_cards.copy()

    def deal_card(self):
        if self.num_cards() <= 5:
            self.reset_deck()
        card = Card(random.choice(self.cards))
        self.cards.remove(card.card_id)
        return card

    def num_cards(self):
        return len(self.cards)

    def reset_deck(self):
        self.cards = self.__all_cards.copy()
