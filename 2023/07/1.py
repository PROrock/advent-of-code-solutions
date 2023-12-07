import dataclasses
import sys
from collections import Counter

# class Type(enum.Enum):
#     FIVE_KIND = 45
#     FOUR_KIND = 34
#     FULL_HOUSE = 32
#     THREE_KIND = 23
#     TWO_PAIR = 22
#     ONE_PAIR = 12
#     HIGH_CARD = 1

CARD_VALUES = "AKQJT98765432"[::-1]
VALUE_TO_STRENGTH = {val: i+2 for i, val in enumerate(CARD_VALUES)}


@dataclasses.dataclass
class Hand:
    cards: str
    bid: int

    @property
    def type(self):
        c = Counter(self.cards)
        n_sets = len(c)
        power = (5-n_sets)*10+c.most_common()[0][1]
        return power

    @property
    def sort_key(self):
        # tuple - type, 5 values of cards
        return self.type, *[VALUE_TO_STRENGTH[card] for card in self.cards]


hands = []
while True:
    line = sys.stdin.readline().rstrip("\r\n")
    if not line:
        break

    cards, bid = line.split()
    hands.append(Hand(cards, int(bid)))

hands = sorted(hands, key=lambda h: h.sort_key)
print(sum([(i + 1) * h.bid for i, h in enumerate(hands)]))
