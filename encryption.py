import configparser
import sympy

CONFIG_FILE = "AmTCD.ini"

def load_key():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return int(config.get("main", "keyuser", fallback="496fd2da03559bb5a0c914e28f98902c"), 16)

def generate_prime():
    return sympy.randprime(2**127, 2**128)

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
