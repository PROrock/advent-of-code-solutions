import sys

# while line:= input():
#     print(line)

#
# while True:
#     line= input()
#     print(line)
#     if not line:
#         print("terminating")
#         break


# userInput = sys.stdin.readlines()
# print(userInput)


# while True:
#     userInput = sys.stdin.readline()
#     print(userInput)

while True:
    line=sys.stdin.readline().rstrip("\r\n")
    print("line", line)
    if not line:
        print("terminating")
        break
