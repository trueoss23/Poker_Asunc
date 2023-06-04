cards = {
    '2': 'N',
    '3': 'M',
    '4': 'K',
    '5': 'J',
    '6': 'I',
    '7': 'H',
    '8': 'G',
    '9': 'F',
    'T': 'E',
    'J': 'D',
    'Q': 'C',
    'K': 'B',
    'A': 'A',
}

suit = {
    'c': 'c',
    's': 's',
    'd': 'd',
    'h': 'h',
}


def get_all_cards(cards):
    deck = {}
    for key in cards.keys():
        for elem in suit.keys():
            deck[key + elem] = cards[key]
    return deck


deck = get_all_cards(cards)


class Cards():
    all_cards = tuple(deck)
    dict_strange_of_cards = {elem: cards[elem[0]] for elem in all_cards}
