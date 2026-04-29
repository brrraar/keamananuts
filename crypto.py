import ascon

def encrypt_message(message, key):
    key = key.ljust(16)[:16].encode()
    nonce = b'1234567890123456'

    cipher = ascon.encrypt(key, nonce, b'', message.encode())
    return cipher.hex()


def decrypt_message(cipher_hex, key):
    key = key.ljust(16)[:16].encode()
    nonce = b'1234567890123456'

    try:
        cipher = bytes.fromhex(cipher_hex)
        plain = ascon.decrypt(key, nonce, b'', cipher)

        # Kalau decrypt gagal
        if plain is None:
            return "KODE SALAH!"

        return plain.decode()

    except:
        # Kalau hex rusak / error lain
        return "KODE SALAH!"