import os
def caesar_cipher(text, shift):
    encrypted_text = ""

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            shifted_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            if is_upper:
                shifted_char = shifted_char.upper()
            encrypted_text += shifted_char
        else:
            encrypted_text += char

    return encrypted_text

def caesar_cipher_decrypt(ciphertext, shift):
    return caesar_cipher(ciphertext, -shift)

if __name__ == "__main__":
    text = "Charlemagne@1"
    shift = 3

    encrypted_text = caesar_cipher(text, shift)
    decrypted_text = caesar_cipher_decrypt(encrypted_text, shift)

    print(f"Original Text: {text}")
    print(f"Encrypted Text: {encrypted_text}")
    print(f"Decrypted Text: {decrypted_text}")
