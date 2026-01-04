from cryptography.fernet import Fernet

# --- Encryption Part ---
def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

def decrypt_message(token, key):
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()

# --- Stego Part (Zero Width) ---
def hide_text_in_text(cover_text, secret_msg):
    # Convert secret to binary
    binary = ''.join(format(ord(i), '08b') for i in secret_msg)
    # Zero-width Space (1) and Zero-width Non-Joiner (0)
    hidden = binary.replace('0', '\u200c').replace('1', '\u200b')
    return cover_text + hidden

def reveal_text_from_text(stego_text):
    # Extract only zero-width chars
    hidden = [c for c in stego_text if c in ['\u200c', '\u200b']]
    if not hidden: return "No hidden message found."
    
    binary_str = ''.join(hidden).replace('\u200c', '0').replace('\u200b', '1')
    # Convert binary back to text
    message = ""
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        message += chr(int(byte, 2))
    return message