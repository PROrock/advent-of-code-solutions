import sys

s = 0
while True:
    line = sys.stdin.readline().rstrip("\r\n")
    if not line:
        break

    print(line)
    _, ticket = line.split(": ")
    winning, predicted = ticket.split("| ")
    winning = set([int(i) for i in winning.split()])
    predicted = set([int(i) for i in predicted.split()])
    intersection = winning.intersection(predicted)

    number = 2 ** (len(intersection) - 1) if len(intersection) > 0 else 0
    print(number)
    s += number

print(s)
