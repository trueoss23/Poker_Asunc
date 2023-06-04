from cards import Cards


def get_all_pairs(cards):
    res = []
    for x in cards:
        for y in cards:
            if x != y and (y, x) not in res:
                res.append((x, y))
    return tuple(res)


class Combinations:
    cards = Cards()
    pairs = get_all_pairs(cards.all_cards)


x = Combinations()
c = [elem for elem in x.pairs if elem[0] == '2c']
print(len(c))
