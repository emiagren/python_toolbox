"""
Tool for cracking hashed passwords
"""

import sys
import argparse
import hashlib

def get_parser():
    """Returns a command-line argument parser."""
    parser = argparse.ArgumentParser(description="Password Hash Cracker")
    parser.add_argument("target_hash", help="The hashed password to crack")
    parser.add_argument("wordlist_path", help="Path to the wordlist file")
    parser.add_argument(
        "-a", "--algorithm", default="sha256",
        help="Hashing algorithm used for the hash (default: sha256)"
    )
    return parser

def hash_password(password: str, algorithm: str = "sha256") -> str:
    """
    Hash a password using the specified hashing algorithm.
    Default is sha256.
    """
    try:
        hash_object = hashlib.new(algorithm)
    except ValueError:
        sys.exit(f"Error: Unsupported algorithm '{algorithm}'. Please use a valid hashing algorithm.")
    
    hash_object.update(password.encode("utf-8"))
    return hash_object.hexdigest()

def crack_password(target_hash: str, wordlist_path: str, algorithm: str = "sha256") -> str:
    """
    Try to crack the hashed password using a file with a list of passwords.
    """
    try:
        with open(wordlist_path, "r", encoding="utf-8") as file:
            for word in file:
                word = word.strip()
                hashed_word = hash_password(word, algorithm)
                if hashed_word == target_hash:
                    return f"Password found: {word}"
        return "Password not found in wordlist."
    
    except FileNotFoundError:
        return "Error: Wordlist file not found. Please provide a valid path."
    except UnicodeDecodeError:
        return "Error: Unable to decode the wordlist file. Please ensure it is a text file with UTF-8 encoding."

def main():
    """Main function for parsing arguments and cracking the password."""
    parser = get_parser()
    args = parser.parse_args()

    # Crack the password
    result = crack_password(args.target_hash, args.wordlist_path, args.algorithm)
    print(result)

if __name__ == "__main__":
    main()
