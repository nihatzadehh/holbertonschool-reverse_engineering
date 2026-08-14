#!/usr/bin/python3

from z3 import *

# Initialize solver
s = Solver()

# Create symbolic variables for each character in the flag
flag_length = 30  # Based on the maximum offset checked (0x1d)
flag = [BitVec(f'flag_{i}', 8) for i in range(flag_length)]

# Add constraints for printable ASCII characters
for c in flag:
    s.add(c >= 32, c <= 126)

# First character must be 'H'
s.add(flag[0] == ord('H'))

# Define all the function constraints based on the disassembly
# Each function takes 3 characters and must return a specific value

# funcOne(flag[0], flag[1], flag[2]) == 0x7a73e0
s.add((flag[0] * flag[1] + flag[2]) == 0x7a73e0)

# funcTwo(flag[1], flag[2], flag[3]) == 0x396c
s.add((flag[1] * flag[2] - flag[3]) == 0x396c)

# funcThree(flag[2], flag[3], flag[4]) == 0x295b
s.add((flag[2] + flag[3] * flag[4]) == 0x295b)

# funcFour(flag[3], flag[4], flag[5]) == 0x110aba
s.add((flag[3] * flag[4] * flag[5]) == 0x110aba)

# funcFive(flag[4], flag[5], flag[6]) == 0xcfd
s.add((flag[4] ^ flag[5] ^ flag[6]) == 0xcfd)

# funcSix(flag[5], flag[6], flag[7]) == 0x1cb
s.add((flag[5] + flag[6] - flag[7]) == 0x1cb)

# funcSeven(flag[6], flag[7], flag[8]) == 0x6122
s.add((flag[6] * flag[7] + flag[8]) == 0x6122)

# funcEight(flag[7], flag[8], flag[9]) == 0x16b5ac
s.add((flag[7] * flag[8] * flag[9]) == 0x16b5ac)

# funcNine(flag[8], flag[9], flag[10]) == 0x5ce
s.add((flag[8] + flag[9] - flag[10]) == 0x5ce)

# funcTen(flag[9], flag[10], flag[11]) == 0x2d0f
s.add((flag[9] * flag[10] + flag[11]) == 0x2d0f)

# funcEleven(flag[10], flag[11], flag[12]) == 0x10ce2f
s.add((flag[10] * flag[11] * flag[12]) == 0x10ce2f)

# funcTwelve(flag[11], flag[12], flag[13]) == 0x2c6f
s.add((flag[11] + flag[12] + flag[13]) == 0x2c6f)

# funcThirteen(flag[12], flag[13], flag[14]) == 0x133d
s.add((flag[12] * flag[13] - flag[14]) == 0x133d)

# funcFourteen(flag[13], flag[14], flag[15]) == 0xee949
s.add((flag[13] * flag[14] * flag[15]) == 0xee949)

# funcFifteen(flag[14], flag[15], flag[16]) == 0x64d5a
s.add((flag[14] * flag[15] + flag[16]) == 0x64d5a)

# funcSixteen(flag[15], flag[16], flag[17]) == 0xc6c
s.add((flag[15] + flag[16] + flag[17]) == 0xc6c)

# funcSeventeen(flag[16], flag[17], flag[18]) == 0x2d63
s.add((flag[16] * flag[17] - flag[18]) == 0x2d63)

# funcEighteen(flag[17], flag[18], flag[19]) == 0x105869
s.add((flag[17] * flag[18] * flag[19]) == 0x105869)

# funcNineteen(flag[18], flag[19], flag[20]) == 0x13b1
s.add((flag[18] + flag[19] - flag[20]) == 0x13b1)

# funcTwenty(flag[19], flag[20], flag[21]) == 0x319d
s.add((flag[19] * flag[20] + flag[21]) == 0x319d)

# Later checks reuse some functions with different constants
# funcOne(flag[22], flag[23], flag[24]) == 0xc33bd5
s.add((flag[22] * flag[23] + flag[24]) == 0xc33bd5)

# funcTwo(flag[23], flag[24], flag[25]) == 0x4201
s.add((flag[23] * flag[24] - flag[25]) == 0x4201)

# funcThree(flag[24], flag[25], flag[26]) == 0x2d2d
s.add((flag[24] + flag[25] * flag[26]) == 0x2d2d)

# funcFour(flag[25], flag[26], flag[27]) == 0x104645
s.add((flag[25] * flag[26] * flag[27]) == 0x104645)

# funcFive(flag[26], flag[27], flag[28]) == 0xca6
s.add((flag[26] ^ flag[27] ^ flag[28]) == 0xca6)

# funcSix(flag[27], flag[28], flag[29]) == 0xfffffc9f (interpreted as -865)
s.add((flag[27] + flag[28] - flag[29]) == -865)

# Solve and print the flag
if s.check() == sat:
    m = s.model()
    solution = ''.join([chr(m.eval(c).as_long()) for c in flag])
    print("Found flag:", solution)
else:
    print("No solution found")