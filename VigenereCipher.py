"""Vigenere Cipher Decryption Tool

Interactive tool to decrypt Vigenere cipher text using a provided key.
Prompts user for the encryption key and ciphertext, then displays the decrypted plaintext.
"""


def decrypt_vigenere(ciphertext, key):
    """
    Decrypt Vigenere cipher text using the given key.
    
    Args:
        ciphertext: The encrypted text to decrypt
        key: The key used for encryption
    
    Returns:
        The decrypted plaintext
    """
    plaintext = []
    key = key.upper()
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            # Get the key character for shifting
            shift = ord(key[key_index % len(key)]) - ord('A')
            
            # Decrypt: shift backwards by key value
            if char.isupper():
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            
            plaintext.append(decrypted_char)
            key_index += 1
        else:
            # Keep non-alphabetic characters as-is
            plaintext.append(char)
    
    return ''.join(plaintext)


def main():
    print("=== Vigenere Cipher Decryption ===\n")
    
    # Prompt for key
    key = input("Enter the encryption key: ").strip()
    if not key:
        print("Error: Key cannot be empty.")
        return
    
    # Validate key contains only alphabetic characters
    if not key.isalpha():
        print("Error: Key must contain only alphabetic characters.")
        return
    
    # Prompt for ciphertext
    print("Enter the ciphertext:")
    ciphertext = input().strip()
    if not ciphertext:
        print("Error: Ciphertext cannot be empty.")
        return
    
    # Decrypt and display
    plaintext = decrypt_vigenere(ciphertext, key)
    
    print("\n=== Results ===")
    print(f"Key:        {key.upper()}")
    print(f"Ciphertext: {ciphertext}")
    print()
    print()
    print(f"Plaintext:  {plaintext}")


if __name__ == "__main__":
    main()
