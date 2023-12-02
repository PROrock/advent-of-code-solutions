# let's ignore EOF for now
# discuss with others later
import string
import sys
from itertools import dropwhile

s = 0
# while line:= input():
while True:
    line=sys.stdin.readline().rstrip("\r\n")
    if not line:
        break
    # print(line)
    digits = next(dropwhile(lambda x: x not in string.digits, line))
    # print(list(digits))
    first = next(dropwhile(lambda x: x not in string.digits, line))
    last = next(dropwhile(lambda x: x not in string.digits, reversed(line)))
    number = 10 * int(first) + int(last)
    # print(number)
    s += number

print(s)
