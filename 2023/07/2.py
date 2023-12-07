import dataclasses
import re
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

JOKER = "J"
CARD_VALUES = "AKQT98765432J"[::-1]
VALUE_TO_STRENGTH = {val: i+1 for i, val in enumerate(CARD_VALUES)}


@dataclasses.dataclass
class Hand:
    cards: str
    bid: int

    @property
    def type(self):
        c = Counter([card for card in self.cards if card != JOKER])
        n_jokers = len(re.findall(JOKER, self.cards))
        n_sets = 1 if n_jokers == 5 else len(c)
        most_common_card_occurence = 0 if n_jokers==5 else c.most_common()[0][1]
        power = (5 - n_sets) * 10 + most_common_card_occurence + n_jokers
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
    hand = Hand(cards, int(bid))
    hands.append(hand)

hands = sorted(hands, key=lambda h: h.sort_key)
print(sum([(i + 1) * h.bid for i, h in enumerate(hands)]))
