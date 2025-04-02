import configparser
import random

CONFIG_FILE = "AmTCD.ini"

def load_key():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    key = int(config.get("main", "keyuser", fallback="534582719245755984509"), 16)
    if key % 2 == 0:
        key += 1
    return key

def is_prime(n):
    if n < 2 or (n % 2 == 0 and n != 2):
        return False
    return all(n % d for d in range(3, int(n**0.5) + 1, 2))

def generate_prime():
    while True:
        num = random.randint(500_000, 1_000_000)
        if is_prime(num):
            return num

def xor_cipher(text, key):
    key_str = str(key)
    return "".join(chr(ord(c) ^ ord(key_str[i % len(key_str)])) for i, c in enumerate(text))

def encrypt(text):
    key = load_key()
    new_key = generate_prime()
    combined_key = key * new_key
    encrypted_text = xor_cipher(text, new_key)
    return f"{combined_key}\n{encrypted_text}"

def decrypt(encrypted_data):
    key = load_key()
    lines = encrypted_data.split("\n", 1)
    if len(lines) < 2:
        raise ValueError("Неверный формат файла!")
    combined_key = int(lines[0])
    encrypted_text = lines[1]
    new_key = combined_key // key
    return xor_cipher(encrypted_text, new_key)
