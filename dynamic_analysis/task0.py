#!/usr/bin/python3
from z3 import *

def solve_flag():
    s = Solver()
    
    # Create 24 8-bit variables for the flag content
    flag_chars = [BitVec(f'char_{i}', 8) for i in range(24)]
    
    # Initialize state variables
    var_4ch = BitVecVal(0, 32)
    var_48h = BitVecVal(1, 32)
    var_44h = BitVecVal(0, 32)
    var_40h = BitVecVal(1, 32)
    
    # Printable ASCII constraints
    for c in flag_chars:
        s.add(And(c >= 0x20, c <= 0x7e))
    
    # Process each character
    for i in range(24):
        char_val = ZeroExt(24, flag_chars[i])
        
        # Update var_4ch
        term1 = (i + 1) * char_val
        term2 = term1 * (i + 2)
        var_4ch += term2 % 256
        
        # Update var_48h
        term3 = (7 * i) + char_val
        term4 = (term3 + 0x1f) * 0x214d0215
        term5 = (term4 >> 32) >> 4
        term6 = (term3 >> 31)
        term7 = (term5 - term6) * 0x7b
        term8 = (term3 + 0x1f - term7)
        var_48h *= term8
        
        # Update var_44h
        term9 = (i + 1) * char_val
        term10 = i * i
        term11 = (term9 + term10)
        var_44h += (term11 & 0x1ff) - (term11 >> 31)
        
        # Update var_40h
        term12 = (i + 3) * char_val
        term13 = term12 + 0x11
        var_40h ^= (term13 & 0x3ff) - (term13 >> 31)
    
    # Final computation
    term14 = var_4ch * var_48h
    term15 = term14 + var_44h - var_40h
    term16 = term15 ^ 0xdeadbeef
    term17 = term16 & 0xffffff
    term18 = term14 + term17 - (var_44h * var_40h)
    term19 = term18 - 0x35014542
    term20 = (term19 >> 1) * 0x87e53f15
    term21 = (term20 >> 32) >> 0x12
    term22 = term21 * 0xf1206
    final = term19 - term22
    
    # Final constraint
    s.add(final == 0xae44)
    
    if s.check() == sat:
        model = s.model()
        flag_part = ''.join([chr(model[flag_chars[i]].as_long()) for i in range(24)])
        return f"Holberton{{{flag_part}}}"
    else:
        return "No solution found"

print(solve_flag())