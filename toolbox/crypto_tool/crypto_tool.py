"""
Encryption/decryption tool
"""

import argparse
import sys
from cryptography.fernet import Fernet, InvalidToken

def generate_key():
    """
    Generates a symmetric encryption key and saves it to 'secret.key' file.
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Secret key generated and saved as 'secret.key'")

def load_secret_key(secret_key_file):
    """ Loads the secret key from a file. """
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

def main(args=None):
    """ 
    Parses command-line arguments to encrypt or decrypt a file using a secret key, 
    then calls the appropriate function to perform the specified operation. 
    """
    # Create argument parser
    parser = argparse.ArgumentParser(description="Generate a key, encrypt, or decrypt files.")
    parser.add_argument("operation", choices=["generate_key", "encrypt", "decrypt"],
                        help="Choose 'generate_key' to create a new key, 'encrypt' to encrypt a file, or 'decrypt' to decrypt a file.")
    parser.add_argument("filename", nargs="?", help="The name of the file to encrypt or decrypt (required for encrypt/decrypt operations).")
    parser.add_argument("secret_keyfile", nargs="?", help="The file containing the secret key (required for encrypt/decrypt operations).")

    # Parse the arguments from args if provided, otherwise use sys.argv
    parsed_args = parser.parse_args(args if args is not None else sys.argv[1:])

    if parsed_args.operation == "generate_key":
        generate_key()
    elif parsed_args.operation == "encrypt":
        if not parsed_args.filename or not parsed_args.secret_keyfile:
            print("Error: 'encrypt' operation requires a filename and a secret key file.")
            sys.exit(1)
        secret_key = load_secret_key(parsed_args.secret_keyfile)
        encrypt_file(parsed_args.filename, secret_key)
    elif parsed_args.operation == "decrypt":
        if not parsed_args.filename or not parsed_args.secret_keyfile:
            print("Error: 'decrypt' operation requires a filename and a secret key file.")
            sys.exit(1)
        secret_key = load_secret_key(parsed_args.secret_keyfile)
        decrypt_file(parsed_args.filename, secret_key)

if __name__ == "__main__":
    main()
