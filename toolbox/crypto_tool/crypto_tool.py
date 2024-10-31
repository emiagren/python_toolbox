"""
Encryption/decryption tool
"""

import argparse
import sys
from cryptography.fernet import Fernet, InvalidToken

def load_secret_key(secret_key_file):
    """Loads the secret key from a file."""
    try:
        with open(secret_key_file, 'rb') as file:
            key = file.read()
        return key
    except FileNotFoundError:
        print(f"Error: Secret key file '{secret_key_file}' not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading secret key file '{secret_key_file}': {e}")
        sys.exit(1)
    
def encrypt_file(filename, key):
    """ Encrypts the file using the provided secret key. """
    fernet = Fernet(key)

    # Read the file content
    try:
        with open(filename, 'rb') as file:
            file_data = file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except IOError as e:
        print(f"Error reading file '{filename}': {e}")
        return

    # Encrypt the data
    encrypted_data = fernet.encrypt(file_data)

    # Save the encrypted data to a new file
    encrypted_filename = filename + '.encrypted'
    try:
        with open(encrypted_filename, 'wb') as file:
            file.write(encrypted_data)
        print(f"File encrypted and saved as {encrypted_filename}")
    except IOError as e:
        print(f"Error saving encrypted file '{encrypted_filename}': {e}")

def decrypt_file(filename, key):
    """ Decrypts the file using the provided secret key. """
    fernet = Fernet(key)

    # Read the encrypted file content
    try:
        with open(filename, 'rb') as file:
            encrypted_data = file.read()
    except FileNotFoundError:
        print(f"Error: Encrypted file '{filename}' not found.")
        return
    except IOError as e:
        print(f"Error reading encrypted file '{filename}': {e}")
        return

    # Try to decrypt the data
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except InvalidToken:
        print("Decryption failed. Incorrect secret key or corrupted file.")
        return

    # Save the decrypted data to a new file
    decrypted_filename = filename.replace('.encrypted', '')
    try:
        with open(decrypted_filename, 'wb') as file:
            file.write(decrypted_data)
            print(f"Dekrypterad text: {decrypted_data}")  
        print(f"File decrypted and saved as {decrypted_filename}")
    except IOError as e:
        print(f"Error saving decrypted file '{decrypted_filename}': {e}")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Encrypt or Decrypt files using a secret key.")
    parser.add_argument("operation", choices=["encrypt", "decrypt"],
                        help="Choose 'encrypt' or 'decrypt'")
    parser.add_argument("filename", help="The name of the file to encrypt or decrypt")
    parser.add_argument("secret_keyfile", help="The file containing the secret key")

    # Parse the arguments
    args = parser.parse_args()

    # Load the secret key
    secret_key = load_secret_key(args.secret_keyfile)

    # Perform the chosen operation
    if args.operation == "encrypt":
        encrypt_file(args.filename, secret_key)
    elif args.operation == "decrypt":
        decrypt_file(args.filename, secret_key)

if __name__ == "__main__":
    main()
