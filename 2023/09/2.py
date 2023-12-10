import sys


def first_derivative(seq):
    return [b - a for a, b in zip(seq[:-1], seq[1:])]


def predict(seq):
    pyramid = [seq]
    derivative = first_derivative(seq)

    while not all(i == 0 for i in derivative):
        pyramid.append(derivative)
        derivative = first_derivative(derivative)
    value = 0
    for seq in reversed(pyramid):
        new_value = seq[0] - value
        value = new_value
    return value


s = 0
while True:
    line = sys.stdin.readline().rstrip("\r\n")
    if not line:
        break

    seq = [int(i) for i in line.split()]
    number = predict(seq)
    s += number

print(s)
