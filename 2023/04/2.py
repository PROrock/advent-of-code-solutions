import sys
from collections import defaultdict

card_copies = defaultdict(int)
s = 0
while True:
    line = sys.stdin.readline().rstrip("\r\n")
    if not line:
        break

    card, ticket = line.split(": ")
    card = int(card[5:])
    winning, predicted = ticket.split("| ")
    winning = set([int(i) for i in winning.split()])
    predicted = set([int(i) for i in predicted.split()])

    intersection = winning.intersection(predicted)
    for i in range(len(intersection)):
        card_copies[card+i+1] += card_copies[card] + 1  # +1 for original

    s += card_copies[card] + 1

print(s)
