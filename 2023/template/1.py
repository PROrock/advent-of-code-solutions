import sys

s = 0
while True:
    line=sys.stdin.readline().rstrip("\r\n")
    if not line:
        break

    print(line)

    number = 0
    print(number)
    s += number

print(s)
