import string

START = ord("a")
CHARSET = string.ascii_lowercase[:16]

def decode_b16(cipher):
    decoded = ""
    
    for i in range(0, len(cipher), 2):
        char1Index = int("{0:04b}".format(CHARSET.index(cipher[i])),2)
        char2Index = int("{0:04b}".format(CHARSET.index(cipher[i+1])),2)
        decoded += chr(char1Index * 16 + char2Index)
    return decoded

def caesar_deshift(c,k):
    return CHARSET[((CHARSET.index(c) - 1) - ord(k) + 2 * START + len(CHARSET)) % len(CHARSET)]

def decrypt(cipher, key):
    b16 = ""
    for i, c in enumerate(cipher):
        b16 += caesar_deshift(c, key[i % len(key)])
    
    return decode_b16(b16)

def brute_force_decrypt_oneLetterKey(ciphertext):
    for letter in string.ascii_lowercase:
        decrypted_text = decrypt(ciphertext, letter)
        print(f"Key: {letter}, Decrypted text: {decrypted_text}")


cipher = "jikmkjgekjkckjkbknkjlhgekflgkjgekbkfkpknkcklgekfgekbkdlkkjgcgejlkjgekckjkjkigelikdgekfkhligekkkflhligc"
brute_force_decrypt_oneLetterKey(cipher)