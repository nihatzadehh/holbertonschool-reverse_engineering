#!/usr/bin/python3
import struct

# Replace these bytes with what you got from GDB
encrypted_flag = bytes.fromhex("""
49 00 ed eb 78 a3 f0 4e 4a 99 13 50 f8 56 96 45
85 15 91 0e a6 8a bf 0d 68 28 d3 73 68 30 48 ce
6d 8d d0 29 7a a5 23 73 d8 56 ea e1 5f 60 5a
""".replace(" ", "").replace("\n", ""))

def ror(val, bits):
    return ((val >> bits) | (val << (8 - bits))) & 0xFF

def prng(seed):
    seed[0] = (seed[0] * 0x1337 + 0x5) & 0xFFFFFFFF
    return (seed[0] >> 16) & 0xFF

def decrypt(encrypted):
    seed = [0x3039]
    decrypted = bytearray()
    
    # Try all possible operation orders
    for reverse_order in [False, True]:
        seed[0] = 0x3039  # Reset seed
        temp_dec = bytearray()
        prng_bytes = [prng(seed) for _ in range(len(encrypted))]
        
        for i in range(len(encrypted)):
            b = encrypted[i]
            
            if reverse_order:
                # Order: XOR → ROR → ADD
                b = (b + 0x5B) & 0xFF
                b = ror(b, 3)
                b ^= prng_bytes[i]
            else:
                # Order: ADD → ROR → XOR
                b ^= prng_bytes[i]
                b = ror(b, 3)
                b = (b + 0x5B) & 0xFF
                
            temp_dec.append(b)
        
        # Check for flag pattern
        dec_str = temp_dec.decode('latin-1')
        if "Holberton{" in dec_str:
            start = dec_str.index("Holberton{")
            end = dec_str.index("}", start) + 1
            return dec_str[start:end]
    
    return "Flag not found in any operation order"

flag = decrypt(encrypted_flag)
print(f"Result: {flag}")