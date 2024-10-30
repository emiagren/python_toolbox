"""
Tool for cracking hashed passwords
"""

import hashlib

def hash_password(password: str, algorithm: str = "sha256") -> str:
    """
    Hash a password using the specified hashing algorithm.
    Default is sha256.
    """
    hash_object = hashlib.new(algorithm)
    hash_object.update(password.encode('utf-8'))
    return hash_object.hexdigest()

def crack_password(target_hash: str, wordlist_path: str, algorithm: str = "sha256") -> str:
    """
    Try to crack the hashed password using a file with a list of passwords.
    """
    try:
        with open(wordlist_path, 'r', encoding="utf-8") as file:
            for word in file:
                word = word.strip()  # Remove any whitespace or newline characters
                hashed_word = hash_password(word, algorithm)

                if hashed_word == target_hash:
                    return f"Password found: {word}"

        return "Password not found in wordlist."

    except FileNotFoundError:
        return "Wordlist file not found. Please provide a valid path."

if __name__ == "__main__":
    # Get user inputs
    INPUT_HASH = input("Enter the hashed password: ")
    WORDLIST_FILE_PATH = input("Enter the path to the wordlist file: ")
    INPUT_ALGORITHM = input("Enter the hashing algorithm (default is sha256): ") or "sha256"

    # Crack the password
    print(crack_password(INPUT_HASH, WORDLIST_FILE_PATH, INPUT_ALGORITHM))
